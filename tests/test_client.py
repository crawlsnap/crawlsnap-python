"""Facade tests using httpx.MockTransport — no network."""

from __future__ import annotations

import asyncio

import httpx
import pytest

import crawlsnap
from crawlsnap import (
    CrawlSnap,
    CrawlSnapError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
)


def _ok(data: dict) -> httpx.Response:
    return httpx.Response(
        200,
        json={"data": data, "is_success": True, "message": "Success", "response_code": 200},
        headers={"x-request-id": "req_ok"},
    )


def _err(status: int, message: str) -> httpx.Response:
    return httpx.Response(
        status,
        json={"data": None, "is_success": False, "message": message, "response_code": status},
        headers={"x-request-id": "req_err"},
    )


def _make_handler():
    state = {"url_calls": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        params = dict(request.url.params)
        if path == "/v1/ioc/search/ip":
            return _ok({
                "hash_id": "h", "search_type": "ip", "ip": params.get("query"),
                "reputation": 3, "as_owner": "GOOGLE", "tags": ["dns"],
            })
        if path == "/v1/ioc/search/domain":
            return _err(404, "No IoC data found")
        if path == "/v1/ioc/search/hash":
            return _err(402, "Monthly quota exceeded")
        if path == "/v1/ioc/search/url":
            state["url_calls"] += 1
            if state["url_calls"] == 1:
                return httpx.Response(
                    429,
                    headers={"Retry-After": "0", "x-request-id": "req_429"},
                    json={"data": None, "is_success": False, "message": "Daily limit", "response_code": 429},
                )
            return _ok({"hash_id": "h", "search_type": "url", "url": params.get("query")})
        if path == "/v1/subdo-snap/scan":
            if not params.get("cursor"):
                return _ok({"hash_id": "h", "search_type": "domain", "subdomains": [{"subdomain": "a.example.com"}], "cursor": "c1", "count": 2})
            return _ok({"hash_id": "h", "search_type": "domain", "subdomains": [{"subdomain": "b.example.com"}], "cursor": "", "count": 2})
        if path == "/v1/sport-snap/channels/bein-connect-turkey":
            return _ok({
                "slug": "bein-connect-turkey", "name": "beIN CONNECT Turkey",
                "country": "Turkey",
                "broadcast_rights": [{"competition": "England - Premier League", "year_start": 2024, "year_end": 2027}],
                "updated_at": "2026-07-05T10:00:00Z",
            })
        if path == "/v1/sport-snap/channels/bein-connect-turkey/schedule":
            return _ok({
                "slug": "bein-connect-turkey", "name": "beIN CONNECT Turkey",
                "entries": [{
                    "date": "2026-07-06", "kickoff_utc": "2026-07-06T19:00:00Z",
                    "match_id": 5542814, "match_title": "Brazil vs Norway",
                    "competition": "Friendly",
                }],
                "updated_at": "2026-07-05T10:00:00Z",
            })
        if path == "/v1/sport-snap/matches/5542814":
            return _ok({
                "id": 5542814, "status": "finished",
                "competition": {"name": "Friendly"},
                "home_team": {"name": "Brazil"}, "away_team": {"name": "Norway"},
                "score": {"home": 2, "away": 1},
                "events": [], "stats": [],
                "broadcasts": [{"country": "Turkey", "country_slug": "turkey",
                                "channels": [{"name": "beIN CONNECT Turkey", "slug": "bein-connect-turkey"}]}],
                "updated_at": "2026-07-05T10:00:00Z",
            })
        if path == "/v1/sport-snap/matches/404":
            return _err(404, "Unknown match id")
        if path == "/v1/sport-snap/countries/turkey/channels":
            return _ok({
                "country": "Turkey", "country_slug": "turkey",
                "channels": [{"name": "beIN CONNECT Turkey", "slug": "bein-connect-turkey",
                              "last_seen": "2026-07-05T10:00:00Z"}],
                "updated_at": "2026-07-05T10:00:00Z",
            })
        if path == "/v1/sport-snap/schedules/2026-07-05":
            return _ok({
                "date": "2026-07-05",
                "competitions": [{"competition": "Friendly", "matches": [{
                    "id": 5542814, "title": "Brazil vs Norway", "status": "scheduled",
                    "kickoff_utc": "2026-07-06T19:00:00Z",
                    "channels": [{"name": "beIN CONNECT Turkey", "slug": "bein-connect-turkey"}],
                }]}],
                "updated_at": "2026-07-05T10:00:00Z",
            })
        return httpx.Response(500, json={"data": None, "is_success": False, "message": f"unexpected {path}", "response_code": 500})

    return handler, state


def _client(max_retries: int = 2):
    handler, state = _make_handler()
    client = CrawlSnap(api_key="sk-cs-test", max_retries=max_retries, transport=httpx.MockTransport(handler))
    return client, state


def test_success_returns_typed_data():
    client, _ = _client()
    ip = client.vector_snap.ip("8.8.8.8")
    assert ip.as_owner == "GOOGLE"
    assert ip.ip == "8.8.8.8"
    assert ip.tags == ["dns"]


def test_pinned_version_hits_same_endpoint_and_is_cached():
    client, _ = _client()
    # Pinning a single product's API version returns the typed payload just
    # like the default (latest) accessor, and the pinned instance is cached.
    assert client.vector_snap.v1.ip("8.8.8.8").as_owner == "GOOGLE"
    assert client.vector_snap.v1 is client.vector_snap.v1


def test_not_found_raises():
    client, _ = _client()
    with pytest.raises(NotFoundError):
        client.vector_snap.domain("nope.example")


def test_quota_exceeded_raises():
    client, _ = _client()
    with pytest.raises(QuotaExceededError) as exc:
        client.vector_snap.hash("deadbeef")
    assert exc.value.status_code == 402
    assert exc.value.request_id == "req_err"


def test_retry_then_success():
    client, state = _client(max_retries=2)
    res = client.vector_snap.url("https://x.com")
    assert res.url == "https://x.com"
    assert state["url_calls"] == 2  # one 429, then a retry that succeeded


def test_rate_limit_exhausted_raises():
    client, _ = _client(max_retries=0)  # no retries -> the 429 surfaces
    with pytest.raises(RateLimitError) as exc:
        client.vector_snap.url("https://x.com")
    assert exc.value.retry_after == 0.0


def test_pagination_iterates_all_pages():
    client, _ = _client()
    assert list(client.subdo_snap.scan_iter("example.com")) == [
        {"subdomain": "a.example.com"},
        {"subdomain": "b.example.com"},
    ]


def test_raw_response():
    client, _ = _client()
    raw = client.vector_snap.ip("8.8.8.8", raw_response=True)
    assert raw.status_code == 200
    assert raw.request_id == "req_ok"
    assert raw.data.as_owner == "GOOGLE"


def test_module_level_singleton():
    handler, _ = _make_handler()
    crawlsnap.init(api_key="sk-cs-test", max_retries=0, transport=httpx.MockTransport(handler))
    assert crawlsnap.vector_snap.ip("8.8.8.8").as_owner == "GOOGLE"


def test_uninitialized_raises(monkeypatch):
    monkeypatch.setattr(crawlsnap, "_default_client", None)
    with pytest.raises(CrawlSnapError):
        _ = crawlsnap.vector_snap


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("CRAWLSNAP_API_KEY", raising=False)
    with pytest.raises(CrawlSnapError):
        CrawlSnap()


def test_default_version_is_stable_not_latest():
    # A direct (unpinned) call targets the product's pinned default version,
    # which must not drift on its own — it equals the explicit .v1 endpoint.
    client, _ = _client()
    assert client.vector_snap._version == "v1"
    assert client.vector_snap.v1._version == "v1"
    # Pinning is per-product: pinning VectorSnap leaves PulseSnap untouched.
    assert client.pulse_snap._version == "v1"


# --------------------------------------------------------------------------
# SportSnap
# --------------------------------------------------------------------------


def test_sport_snap_channel():
    client, _ = _client()
    ch = client.sport_snap.channel("bein-connect-turkey")
    assert ch.slug == "bein-connect-turkey"
    assert ch.broadcast_rights[0].competition == "England - Premier League"
    assert ch.broadcast_rights[0].year_end == 2027


def test_sport_snap_channel_schedule():
    client, _ = _client()
    sched = client.sport_snap.channel_schedule("bein-connect-turkey")
    assert sched.entries[0].match_id == 5542814
    assert sched.entries[0].match_title == "Brazil vs Norway"


def test_sport_snap_match():
    client, _ = _client()
    match = client.sport_snap.match(5542814)
    assert match.status == "finished"
    assert match.score.home == 2 and match.score.away == 1
    assert match.broadcasts[0].country_slug == "turkey"
    assert match.broadcasts[0].channels[0].slug == "bein-connect-turkey"


def test_sport_snap_match_not_found():
    client, _ = _client()
    with pytest.raises(NotFoundError):
        client.sport_snap.match(404)


def test_sport_snap_country_channels():
    client, _ = _client()
    cc = client.sport_snap.country_channels("turkey")
    assert cc.country == "Turkey"
    assert cc.channels[0].slug == "bein-connect-turkey"


def test_sport_snap_daily_schedule_accepts_date_object():
    import datetime

    client, _ = _client()
    day = client.sport_snap.daily_schedule(datetime.date(2026, 7, 5))
    assert day.competitions[0].matches[0].title == "Brazil vs Norway"
    # Same endpoint via a plain string.
    assert client.sport_snap.daily_schedule("2026-07-05").competitions[0].competition == "Friendly"


def test_sport_snap_version_pinning():
    client, _ = _client()
    assert client.sport_snap.v1.channel("bein-connect-turkey").slug == "bein-connect-turkey"
    assert client.sport_snap.v1 is client.sport_snap.v1


# --------------------------------------------------------------------------
# Async client — same surface, awaitable.
# --------------------------------------------------------------------------


def _async_client(max_retries: int = 2):
    from crawlsnap import AsyncCrawlSnap

    handler, state = _make_handler()
    client = AsyncCrawlSnap(
        api_key="sk-cs-test", max_retries=max_retries, transport=httpx.MockTransport(handler)
    )
    return client, state


def test_async_success_returns_typed_data():
    async def run():
        client, _ = _async_client()
        try:
            ip = await client.vector_snap.ip("8.8.8.8")
            assert ip.as_owner == "GOOGLE"
            assert ip.ip == "8.8.8.8"
        finally:
            await client.close()

    asyncio.run(run())


def test_async_not_found_raises():
    async def run():
        client, _ = _async_client()
        try:
            with pytest.raises(NotFoundError):
                await client.vector_snap.domain("nope.example")
        finally:
            await client.close()

    asyncio.run(run())


def test_async_retry_then_success():
    async def run():
        client, state = _async_client(max_retries=2)
        try:
            res = await client.vector_snap.url("https://x.com")
            assert res.url == "https://x.com"
            assert state["url_calls"] == 2
        finally:
            await client.close()

    asyncio.run(run())


def test_async_pagination_iterates_all_pages():
    async def run():
        client, _ = _async_client()
        try:
            out = [sub async for sub in client.subdo_snap.scan_iter("example.com")]
            assert out == [{"subdomain": "a.example.com"}, {"subdomain": "b.example.com"}]
        finally:
            await client.close()

    asyncio.run(run())


def test_async_sport_snap_match():
    async def run():
        client, _ = _async_client()
        try:
            match = await client.sport_snap.match(5542814)
            assert match.status == "finished"
            assert match.home_team.name == "Brazil"
        finally:
            await client.close()

    asyncio.run(run())


def test_async_context_manager():
    async def run():
        from crawlsnap import AsyncCrawlSnap

        handler, _ = _make_handler()
        async with AsyncCrawlSnap(
            api_key="sk-cs-test", max_retries=0, transport=httpx.MockTransport(handler)
        ) as client:
            assert (await client.vector_snap.ip("8.8.8.8")).as_owner == "GOOGLE"

    asyncio.run(run())

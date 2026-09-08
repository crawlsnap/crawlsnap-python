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
    state = {"url_calls": 0, "serp_params": {}}

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
        if path == "/v1/sport-snap/livescores":
            return _ok({
                "sport": "soccer", "updated": "2026-07-05 10:00:00",
                "matches": [{"id": "5542814", "game": "Brazil vs Norway", "result": "2 - 1", "status": "FT"}],
            })
        if path == "/v1/sport-snap/matches":
            return _ok({
                "competitions": [{
                    "competition": "Friendly",
                    "fixtures": [{"fixture_id": "5542814", "team1_name": "Brazil", "team2_name": "Norway"}],
                }],
            })
        if path == "/v1/sport-snap/match/5542814":
            return _ok({
                "competition": {"competition": "Friendly", "slug": "friendly"},
                "fixture": {"fixture_id": "5542814", "game": "Brazil vs Norway", "status": "FT", "result": "2 - 1"},
            })
        if path == "/v1/sport-snap/match/404":
            return _err(404, "Unknown match id")
        if path == "/v1/sport-snap/competitions":
            return _ok({
                "competitions": {
                    "comp_popular": [{"competition_id": "1", "name": "Premier League", "slug": "premier-league", "country": "England"}],
                },
            })
        if path == "/v1/sport-snap/competitions/england/premier-league":
            return _ok({
                "competition": {"competition_id": "1", "competition": "Premier League", "slug": "premier-league", "country": "England"},
                "fixtures": [{"fixture_id": "77", "team1_name": "Arsenal", "team2_name": "Chelsea"}],
            })
        if path == "/v1/sport-snap/countries/brazil":
            return _ok({"team": {"title": "Brazil", "slug": "brazil", "country": "Brazil", "nat_team": "1"}})
        if path == "/v1/sport-snap/channels":
            return _ok({
                "channels": [{"channel_id": "9", "name": "beIN CONNECT Turkey", "slug": "bein-connect-turkey", "country": "Turkey"}],
            })
        if path == "/v1/sport-snap/channels/bein-connect-turkey/info":
            return _ok({
                "channel": {"channel_id": "9", "slug": "bein-connect-turkey", "name": "beIN CONNECT Turkey", "platform": "streaming"},
                "tv_rights": [{"channel_id": "9", "name": "beIN Sports"}],
            })
        if path == "/v1/sport-snap/channels/bein-connect-turkey/repeat":
            page = {"channel": {"slug": "bein-connect-turkey", "name": "beIN CONNECT Turkey"}}
            if params.get("cursor") == "/channels/bein-connect-turkey/repeat/?direction=next&start=2":
                return _ok({**page, "fixtures": [{"fixture_id": "2", "game": "B vs C"}], "fixtures_next": None, "fixtures_prev": "/channels/bein-connect-turkey/repeat/?direction=previous&start=1"})
            return _ok({**page, "fixtures": [{"fixture_id": "1", "game": "A vs B"}], "fixtures_next": "/channels/bein-connect-turkey/repeat/?direction=next&start=2", "fixtures_prev": None})
        if path == "/v1/sport-snap/news":
            return _ok({"articles": [{"article_id": "321", "title": "Transfer news", "slug": "transfer-news"}]})
        if path == "/v1/sport-snap/search/all":
            return _ok({"results": [{"type": "team", "url": "/teams/spain/barcelona/", "title": "Barcelona"}]})
        if path == "/v1/serp/search":
            state["serp_params"] = params
            return _ok({
                "query": params.get("q"),
                "page": int(params.get("page", 1)),
                "engine": "google",
                "results": [{
                    "rank": 1,
                    "title": "Operator pattern - Kubernetes",
                    "url": "https://kubernetes.io/docs/concepts/extend-kubernetes/operator/",
                    "domain": "kubernetes.io",
                    "snippet": "Operators are software extensions to Kubernetes ...",
                }],
                "suggestions": ["kubernetes operator sdk"],
                "elapsed_ms": 912,
            })
        if path == "/v1/sport-snap/player/messi/123":
            return _ok({"profile": {"id": "123", "slug": "messi", "name": "Lionel Messi", "position": "Forward"}})
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


def test_sport_snap_livescores():
    client, _ = _client()
    board = client.sport_snap.livescores()
    assert board.sport == "soccer"
    assert board.matches[0].game == "Brazil vs Norway"
    assert board.matches[0].result == "2 - 1"


def test_sport_snap_matches():
    client, _ = _client()
    fx = client.sport_snap.matches("TR")
    assert fx.competitions[0].competition == "Friendly"
    assert fx.competitions[0].fixtures[0].team1_name == "Brazil"


def test_sport_snap_match():
    client, _ = _client()
    match = client.sport_snap.match(5542814)
    assert match.competition.competition == "Friendly"
    assert match.fixture.fixture_id == "5542814"
    assert match.fixture.result == "2 - 1"


def test_sport_snap_match_not_found():
    client, _ = _client()
    with pytest.raises(NotFoundError):
        client.sport_snap.match(404)


def test_sport_snap_competitions():
    client, _ = _client()
    cat = client.sport_snap.competitions()
    assert cat.competitions.comp_popular[0].name == "Premier League"


def test_sport_snap_competition():
    client, _ = _client()
    comp = client.sport_snap.competition("england", "premier-league")
    assert comp.competition.slug == "premier-league"
    assert comp.fixtures[0].team1_name == "Arsenal"


def test_sport_snap_national_team():
    client, _ = _client()
    team = client.sport_snap.national_team("brazil")
    assert team.team.title == "Brazil"


def test_sport_snap_channels():
    client, _ = _client()
    chs = client.sport_snap.channels("TR")
    assert chs.channels[0].slug == "bein-connect-turkey"


def test_sport_snap_channel_info():
    client, _ = _client()
    info = client.sport_snap.channel_info("bein-connect-turkey")
    assert info.channel.name == "beIN CONNECT Turkey"
    assert info.tv_rights[0].name == "beIN Sports"


def test_sport_snap_channel_repeats_cursor_paging():
    client, _ = _client()
    first = client.sport_snap.channel_repeats("bein-connect-turkey", "TR")
    assert first.fixtures[0].fixture_id == "1"
    assert first.fixtures_prev is None
    second = client.sport_snap.channel_repeats("bein-connect-turkey", "TR", cursor=first.fixtures_next)
    assert second.fixtures[0].fixture_id == "2"
    assert second.fixtures_next is None


def test_sport_snap_news():
    client, _ = _client()
    feed = client.sport_snap.news()
    assert feed.articles[0].title == "Transfer news"


def test_sport_snap_search_all():
    client, _ = _client()
    res = client.sport_snap.search_all("barcelona")
    assert res.results[0].title == "Barcelona"
    assert res.results[0].type == "team"


def test_sport_snap_player():
    client, _ = _client()
    player = client.sport_snap.player("messi", 123)
    assert player.profile.name == "Lionel Messi"


def test_sport_snap_version_pinning():
    client, _ = _client()
    assert client.sport_snap.v1.livescores().sport == "soccer"
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
            assert match.competition.competition == "Friendly"
            assert match.fixture.fixture_id == "5542814"
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


# --------------------------------------------------------------------------
# SerpApi
# --------------------------------------------------------------------------


def test_serp_api_search():
    client, state = _client()
    page = client.serp_api.search("kubernetes operator")
    assert page.engine == "google"
    assert page.results[0].rank == 1
    assert page.results[0].domain == "kubernetes.io"
    # The target URL is real, never a search-engine redirector.
    assert page.results[0].url.startswith("https://kubernetes.io/")
    assert page.suggestions == ["kubernetes operator sdk"]
    # Unset refinements are omitted so the API's own defaults apply.
    assert state["serp_params"] == {"q": "kubernetes operator"}


def test_serp_api_search_refinements_are_sent():
    client, state = _client()
    client.serp_api.search(
        "actions",
        count=20,
        page=2,
        language="de",
        country="de",
        safe=True,
        time_range="month",
        site="github.com",
        filetype="pdf",
    )
    assert state["serp_params"] == {
        "q": "actions", "count": "20", "page": "2", "language": "de", "country": "de",
        "safe": "true", "time_range": "month", "site": "github.com", "filetype": "pdf",
    }


def test_serp_api_version_pinning():
    client, _ = _client()
    assert client.serp_api.v1._version == "v1"


def test_async_serp_api_search():
    async def run():
        client, _ = _async_client()
        try:
            page = await client.serp_api.search("kubernetes operator")
            assert page.results[0].domain == "kubernetes.io"
        finally:
            await client.close()

    asyncio.run(run())

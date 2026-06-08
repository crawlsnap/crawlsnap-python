"""Facade tests using httpx.MockTransport — no network."""

from __future__ import annotations

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

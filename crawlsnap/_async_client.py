"""The asynchronous CrawlSnap client.

``AsyncCrawlSnap`` is the awaitable twin of :class:`crawlsnap.CrawlSnap`: same
constructor, same resource groups, same retry/envelope/error semantics — every
call is a coroutine and pagination is an async generator. It owns an
:class:`httpx.AsyncClient` and shares all IO-free logic with the sync client
via :mod:`crawlsnap._base`.

    import asyncio
    from crawlsnap import AsyncCrawlSnap

    async def main():
        async with AsyncCrawlSnap(api_key="sk-cs-...") as client:
            ip = await client.vector_snap.ip("8.8.8.8")
            print(ip.reputation, ip.as_owner)

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Optional

import httpx

from ._async_resources import AsyncPulseSnap, AsyncSubdoSnap, AsyncVectorSnap
from ._base import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    backoff_delay,
    build_headers,
    is_retryable_status,
    process_response,
)
from ._exceptions import APIConnectionError, APITimeoutError, CrawlSnapError

__all__ = ["AsyncCrawlSnap"]


class AsyncCrawlSnap:
    """Asynchronous CrawlSnap API client.

    :param api_key: Your ``sk-cs-`` key. Falls back to ``$CRAWLSNAP_API_KEY``.
    :param base_url: Override the API host (falls back to ``$CRAWLSNAP_BASE_URL``).
    :param timeout: Per-request timeout in seconds.
    :param max_retries: Retries for 429 / 5xx / connection errors (exp. backoff).
    :param http_client: Supply your own ``httpx.AsyncClient`` (advanced).
    :param transport: Supply a custom ``httpx`` async transport (e.g. for testing).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.AsyncClient] = None,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> None:
        api_key = api_key or os.environ.get("CRAWLSNAP_API_KEY")
        if not api_key:
            raise CrawlSnapError(
                "No API key provided. Pass api_key=... or set CRAWLSNAP_API_KEY."
            )

        self.api_key = api_key
        self.base_url = (
            base_url or os.environ.get("CRAWLSNAP_BASE_URL") or DEFAULT_BASE_URL
        ).rstrip("/")
        self.max_retries = max(0, max_retries)

        if http_client is not None:
            self._client = http_client
            self._owns_client = False
        else:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=timeout,
                transport=transport,
                headers=build_headers(api_key),
            )
            self._owns_client = True

        self.vector_snap = AsyncVectorSnap(self)
        self.pulse_snap = AsyncPulseSnap(self)
        self.subdo_snap = AsyncSubdoSnap(self)

    # -- public lifecycle ------------------------------------------------

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncCrawlSnap":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    # -- internal request pipeline --------------------------------------

    async def _request(
        self,
        path: str,
        params: Dict[str, Any],
        model: Any,
        *,
        raw_response: bool = False,
    ) -> Any:
        attempt = 0
        while True:
            try:
                response = await self._client.get(path, params=params)
            except httpx.TimeoutException as exc:
                if attempt < self.max_retries:
                    await asyncio.sleep(backoff_delay(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(str(exc) or "Request timed out.") from exc
            except httpx.TransportError as exc:
                if attempt < self.max_retries:
                    await asyncio.sleep(backoff_delay(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc) or "Connection error.") from exc

            if is_retryable_status(response.status_code) and attempt < self.max_retries:
                await asyncio.sleep(backoff_delay(attempt, response))
                attempt += 1
                continue

            return process_response(response, model, raw_response=raw_response)

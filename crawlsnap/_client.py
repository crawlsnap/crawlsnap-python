"""The synchronous CrawlSnap client — the canonical entry point.

``CrawlSnap`` owns an :class:`httpx.Client`, applies Bearer auth, retries
transient failures with exponential backoff, unwraps the ``BaseResponse``
envelope, and raises typed exceptions. Resource groups are exposed as
attributes: ``client.vector_snap``, ``client.pulse_snap``,
``client.subdo_snap``, ``client.sport_snap``.

For an awaitable variant with the same surface, see
:class:`crawlsnap.AsyncCrawlSnap`.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import httpx

from ._base import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    RawResponse,
    backoff_delay,
    build_headers,
    is_retryable_status,
    process_response,
)
from ._exceptions import APIConnectionError, APITimeoutError, CrawlSnapError
from ._resources import PulseSnap, SportSnap, SubdoSnap, VectorSnap

__all__ = ["CrawlSnap", "RawResponse"]


class CrawlSnap:
    """Synchronous CrawlSnap API client.

    :param api_key: Your ``sk-cs-`` key. Falls back to ``$CRAWLSNAP_API_KEY``.
    :param base_url: Override the API host (falls back to ``$CRAWLSNAP_BASE_URL``).
    :param timeout: Per-request timeout in seconds.
    :param max_retries: Retries for 429 / 5xx / connection errors (exp. backoff).
    :param http_client: Supply your own ``httpx.Client`` (advanced).
    :param transport: Supply a custom ``httpx`` transport (e.g. for testing).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.Client] = None,
        transport: Optional[httpx.BaseTransport] = None,
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
            self._client = httpx.Client(
                base_url=self.base_url,
                timeout=timeout,
                transport=transport,
                headers=build_headers(api_key),
            )
            self._owns_client = True

        self.vector_snap = VectorSnap(self)
        self.pulse_snap = PulseSnap(self)
        self.subdo_snap = SubdoSnap(self)
        self.sport_snap = SportSnap(self)

    # -- public lifecycle ------------------------------------------------

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "CrawlSnap":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # -- internal request pipeline --------------------------------------

    def _request(
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
                response = self._client.get(path, params=params)
            except httpx.TimeoutException as exc:
                if attempt < self.max_retries:
                    time.sleep(backoff_delay(attempt, None))
                    attempt += 1
                    continue
                raise APITimeoutError(str(exc) or "Request timed out.") from exc
            except httpx.TransportError as exc:
                if attempt < self.max_retries:
                    time.sleep(backoff_delay(attempt, None))
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc) or "Connection error.") from exc

            if is_retryable_status(response.status_code) and attempt < self.max_retries:
                time.sleep(backoff_delay(attempt, response))
                attempt += 1
                continue

            return process_response(response, model, raw_response=raw_response)

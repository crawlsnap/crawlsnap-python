"""The CrawlSnap client — the canonical entry point.

``CrawlSnap`` owns an :class:`httpx.Client`, applies Bearer auth, retries
transient failures with exponential backoff, unwraps the ``BaseResponse``
envelope, and raises typed exceptions. Resource groups are exposed as
attributes: ``client.vector_snap``, ``client.pulse_snap``, ``client.subdo_snap``.
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

import httpx

from ._exceptions import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    CrawlSnapError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    SubscriptionInactiveError,
)
from ._resources import PulseSnap, SubdoSnap, VectorSnap
from ._version import __version__

DEFAULT_BASE_URL = "https://api.crawlsnap.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2

# HTTP statuses worth retrying: rate limit + transient server/upstream failures.
_RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
_RETRY_BASE_DELAY = 0.5
_RETRY_MAX_DELAY = 8.0

_STATUS_TO_ERROR = {
    400: BadRequestError,
    401: AuthenticationError,
    402: QuotaExceededError,
    403: SubscriptionInactiveError,
    404: NotFoundError,
    429: RateLimitError,
}


@dataclass
class RawResponse:
    """The full envelope, returned when a call is made with ``raw_response=True``."""

    status_code: int
    is_success: bool
    data: Any
    message: str
    response_code: Optional[int]
    request_id: Optional[str]
    headers: Mapping[str, str] = field(default_factory=dict)


def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return None  # HTTP-date form is not emitted by this API; ignore it.


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
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Accept": "application/json",
                    "User-Agent": f"crawlsnap-python/{__version__}",
                },
            )
            self._owns_client = True

        self.vector_snap = VectorSnap(self)
        self.pulse_snap = PulseSnap(self)
        self.subdo_snap = SubdoSnap(self)

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
                    self._backoff(attempt, None)
                    attempt += 1
                    continue
                raise APITimeoutError(str(exc) or "Request timed out.") from exc
            except httpx.TransportError as exc:
                if attempt < self.max_retries:
                    self._backoff(attempt, None)
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc) or "Connection error.") from exc

            if response.status_code in _RETRYABLE_STATUS and attempt < self.max_retries:
                self._backoff(attempt, response)
                attempt += 1
                continue

            return self._process(response, model, raw_response=raw_response)

    def _process(self, response: httpx.Response, model: Any, *, raw_response: bool) -> Any:
        request_id = response.headers.get("x-request-id")
        try:
            body: Any = response.json()
        except ValueError:
            body = None

        envelope = body if isinstance(body, dict) else {}
        # `is_success` in the body is authoritative; the HTTP status normally
        # mirrors it, but we honour the body's response_code defensively so a
        # 200-wrapped error (should not happen on the direct API) still raises.
        ok = response.is_success and envelope.get("is_success", response.is_success) is not False
        effective_status = response.status_code
        if not response.is_success or envelope.get("is_success") is False:
            ok = False
            rc = envelope.get("response_code")
            if isinstance(rc, int) and rc >= 400:
                effective_status = rc

        if ok:
            data = envelope.get("data")
            parsed = model.from_dict(data) if (model is not None and isinstance(data, dict)) else data
            if raw_response:
                return RawResponse(
                    status_code=response.status_code,
                    is_success=True,
                    data=parsed,
                    message=envelope.get("message", ""),
                    response_code=envelope.get("response_code"),
                    request_id=request_id,
                    headers=dict(response.headers),
                )
            return parsed

        message = envelope.get("message") or envelope.get("error") or f"HTTP {effective_status}"
        self._raise(effective_status, message, request_id, body, response)

    def _raise(
        self,
        status: int,
        message: str,
        request_id: Optional[str],
        body: Any,
        response: httpx.Response,
    ) -> None:
        kwargs: Dict[str, Any] = {"status_code": status, "request_id": request_id, "body": body}
        if status == 429:
            raise RateLimitError(
                message,
                retry_after=_parse_retry_after(response.headers.get("retry-after")),
                **kwargs,
            )
        error_cls = _STATUS_TO_ERROR.get(status)
        if error_cls is not None:
            raise error_cls(message, **kwargs)
        if status >= 500:
            raise ServerError(message, **kwargs)
        raise APIStatusError(message, **kwargs)

    def _backoff(self, attempt: int, response: Optional[httpx.Response]) -> None:
        delay = min(_RETRY_MAX_DELAY, _RETRY_BASE_DELAY * (2 ** attempt))
        if response is not None and response.status_code == 429:
            retry_after = _parse_retry_after(response.headers.get("retry-after"))
            if retry_after is not None:
                delay = retry_after
        delay += random.uniform(0, _RETRY_BASE_DELAY / 2)  # jitter
        time.sleep(delay)

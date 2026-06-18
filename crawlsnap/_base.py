"""Shared, IO-free building blocks for the sync and async clients.

Everything here is pure (no network, no sleeping): header assembly, envelope
unwrapping, status-to-exception mapping, and backoff-delay computation. The
sync client (:mod:`crawlsnap._client`) and async client
(:mod:`crawlsnap._async_client`) each own the actual request loop but share
this logic so the tricky envelope handling lives in exactly one place.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

import httpx

from ._exceptions import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    SubscriptionInactiveError,
)
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


def build_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": f"crawlsnap-python/{__version__}",
    }


def parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return None  # HTTP-date form is not emitted by this API; ignore it.


def is_retryable_status(status: int) -> bool:
    return status in _RETRYABLE_STATUS


def backoff_delay(attempt: int, response: Optional[httpx.Response]) -> float:
    """Seconds to wait before the next attempt (exp. backoff + jitter, honoring
    ``Retry-After`` on a 429). Pure — the caller does the actual sleeping."""
    delay = min(_RETRY_MAX_DELAY, _RETRY_BASE_DELAY * (2 ** attempt))
    if response is not None and response.status_code == 429:
        retry_after = parse_retry_after(response.headers.get("retry-after"))
        if retry_after is not None:
            delay = retry_after
    return delay + random.uniform(0, _RETRY_BASE_DELAY / 2)  # jitter


def process_response(response: httpx.Response, model: Any, *, raw_response: bool) -> Any:
    """Unwrap the ``BaseResponse`` envelope into typed data, or raise a typed
    error. Shared by both clients — contains no IO."""
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
    _raise(effective_status, message, request_id, body, response)


def _raise(
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
            retry_after=parse_retry_after(response.headers.get("retry-after")),
            **kwargs,
        )
    error_cls = _STATUS_TO_ERROR.get(status)
    if error_cls is not None:
        raise error_cls(message, **kwargs)
    if status >= 500:
        raise ServerError(message, **kwargs)
    raise APIStatusError(message, **kwargs)

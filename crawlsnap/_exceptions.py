"""Exception hierarchy for the CrawlSnap SDK.

    CrawlSnapError                      base for everything raised by the SDK
    ├── APIConnectionError              transport failed (no HTTP response)
    │   └── APITimeoutError             the request timed out
    └── APIStatusError                  the API returned a non-success status
        ├── BadRequestError             400  invalid input
        ├── AuthenticationError         401  missing / invalid API key
        ├── QuotaExceededError          402  out of credits / monthly quota
        ├── SubscriptionInactiveError   403  subscription not active
        ├── NotFoundError               404  no data for the indicator
        ├── RateLimitError              429  daily request limit exceeded
        └── ServerError                 5xx  server / upstream failure

Catch ``CrawlSnapError`` to handle anything the SDK may raise.
"""

from __future__ import annotations

from typing import Any, Optional


class CrawlSnapError(Exception):
    """Base class for all errors raised by the CrawlSnap SDK."""


class APIConnectionError(CrawlSnapError):
    """The request could not reach the API (DNS, connection, TLS, ...)."""

    def __init__(self, message: str = "Connection error.") -> None:
        super().__init__(message)
        self.message = message


class APITimeoutError(APIConnectionError):
    """The request timed out before a response was received."""

    def __init__(self, message: str = "Request timed out.") -> None:
        super().__init__(message)


class APIStatusError(CrawlSnapError):
    """The API responded with a non-success status code."""

    #: Default status code for the subclass; overridden per concrete error.
    status_code: int = 0

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.request_id = request_id
        #: The parsed response body (the BaseResponse envelope), when available.
        self.body = body

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        rid = f" (request_id: {self.request_id})" if self.request_id else ""
        return f"[{self.status_code}] {self.message}{rid}"


class BadRequestError(APIStatusError):
    status_code = 400


class AuthenticationError(APIStatusError):
    status_code = 401


class QuotaExceededError(APIStatusError):
    """Out of credits, or the subscription's monthly quota is exceeded (402)."""

    status_code = 402


class SubscriptionInactiveError(APIStatusError):
    status_code = 403


class NotFoundError(APIStatusError):
    """No IoC data was found for the supplied indicator (404)."""

    status_code = 404


class RateLimitError(APIStatusError):
    """The API key's daily request limit has been exceeded (429)."""

    status_code = 429

    def __init__(self, message: str, *, retry_after: Optional[float] = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        #: Seconds to wait before retrying, parsed from the ``Retry-After`` header.
        self.retry_after = retry_after


class ServerError(APIStatusError):
    """The API or an upstream enrichment service failed (5xx)."""

    status_code = 500


__all__ = [
    "CrawlSnapError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "QuotaExceededError",
    "SubscriptionInactiveError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]

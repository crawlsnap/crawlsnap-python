"""CrawlSnap — official Python SDK for the CrawlSnap data intelligence platform.

Quick start (module-level singleton)::

    import crawlsnap

    crawlsnap.init(api_key="sk-cs-...")          # or set CRAWLSNAP_API_KEY
    ip = crawlsnap.vector_snap.ip("8.8.8.8")
    print(ip.reputation, ip.as_owner)

Advanced (own client instance — multi-key / thread-safe)::

    from crawlsnap import CrawlSnap

    client = CrawlSnap(api_key="sk-cs-...", timeout=30, max_retries=3)
    client.vector_snap.domain("example.com")
"""

from __future__ import annotations

from typing import Any, Optional

from ._client import CrawlSnap, RawResponse
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
from ._version import __version__

# Commonly used response payload types, re-exported for type hints.
from crawlsnap.models.ioc_domain_scan_data import IocDomainScanData
from crawlsnap.models.ioc_hash_scan_data import IocHashScanData
from crawlsnap.models.ioc_ip_scan_data import IocIpScanData
from crawlsnap.models.ioc_url_scan_data import IocUrlScanData
from crawlsnap.models.pulse_domain_scan_data import PulseDomainScanData
from crawlsnap.models.pulse_hash_scan_data import PulseHashScanData
from crawlsnap.models.pulse_ip_scan_data import PulseIpScanData
from crawlsnap.models.pulse_url_scan_data import PulseUrlScanData
from crawlsnap.models.subdo_snap_scan_data import SubdoSnapScanData

_default_client: Optional[CrawlSnap] = None

# Resource names resolved lazily against the singleton (see __getattr__).
_RESOURCE_NAMES = ("vector_snap", "pulse_snap", "subdo_snap")


def init(api_key: Optional[str] = None, **kwargs: Any) -> CrawlSnap:
    """Initialize the module-level singleton client.

    Call once at startup. Accepts the same arguments as :class:`CrawlSnap`
    (``base_url``, ``timeout``, ``max_retries``, ...). Returns the client so
    you can keep a reference if you want one.
    """
    global _default_client
    _default_client = CrawlSnap(api_key, **kwargs)
    return _default_client


def get_client() -> CrawlSnap:
    """Return the singleton created by :func:`init`, or raise if not initialized."""
    if _default_client is None:
        raise CrawlSnapError(
            "crawlsnap is not initialized. Call crawlsnap.init(api_key=...) first, "
            "or create a CrawlSnap(...) instance directly."
        )
    return _default_client


def __getattr__(name: str) -> Any:
    # PEP 562: resolve crawlsnap.vector_snap / .pulse_snap / .subdo_snap to the
    # singleton's resources at access time, with a friendly error if uninitialized.
    if name in _RESOURCE_NAMES:
        return getattr(get_client(), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "init",
    "get_client",
    "CrawlSnap",
    "RawResponse",
    "__version__",
    # exceptions
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
    # response models
    "IocUrlScanData",
    "IocHashScanData",
    "IocIpScanData",
    "IocDomainScanData",
    "PulseUrlScanData",
    "PulseHashScanData",
    "PulseIpScanData",
    "PulseDomainScanData",
    "SubdoSnapScanData",
]

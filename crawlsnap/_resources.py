"""Resource groups exposed on the client: ``vector_snap``, ``pulse_snap``,
``subdo_snap``. Each method submits one indicator and returns the typed
enrichment payload (the unwrapped ``data``), or raises a typed exception.

Per-API versioning
-------------------
Every CrawlSnap data product is versioned independently. Calling a resource
method directly uses that product's *latest* API version::

    client.vector_snap.ip("8.8.8.8")      # latest VectorSnap

To pin one product to a specific API version — without affecting the others —
use its version namespace::

    client.vector_snap.v1.ip("8.8.8.8")   # explicitly VectorSnap v1
    client.pulse_snap.url("https://x")    # still latest PulseSnap

Adding a new API version (e.g. VectorSnap v2)
---------------------------------------------
1. Add the new typed models for v2 (kept alongside the v1 ones so v1 callers
   keep working).
2. Add a ``VectorSnapV2`` implementation class below, with its own ``_PREFIX``
   (``/v2/...``) and return types.
3. Re-base the public ``VectorSnap`` namespace on the new latest
   (``class VectorSnap(_VersionedNamespace, VectorSnapV2)``) and add a ``v2``
   property. Keep the ``v1`` property and ``VectorSnapV1`` intact.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, Type, TypeVar

from crawlsnap.models.ioc_domain_scan_data import IocDomainScanData
from crawlsnap.models.ioc_hash_scan_data import IocHashScanData
from crawlsnap.models.ioc_ip_scan_data import IocIpScanData
from crawlsnap.models.ioc_url_scan_data import IocUrlScanData
from crawlsnap.models.pulse_domain_scan_data import PulseDomainScanData
from crawlsnap.models.pulse_hash_scan_data import PulseHashScanData
from crawlsnap.models.pulse_ip_scan_data import PulseIpScanData
from crawlsnap.models.pulse_url_scan_data import PulseUrlScanData
from crawlsnap.models.subdo_snap_scan_data import SubdoSnapScanData

if TYPE_CHECKING:
    from ._client import CrawlSnap

_R = TypeVar("_R", bound="_Resource")


class _Resource:
    def __init__(self, client: "CrawlSnap") -> None:
        self._client = client


class _VersionedNamespace(_Resource):
    """Public namespace for one data product.

    Inherits the *latest* version's methods (so direct calls use the newest
    API), and exposes ``vN`` properties that return version-pinned instances.
    Pinned instances are created lazily and cached per client.
    """

    def __init__(self, client: "CrawlSnap") -> None:
        super().__init__(client)
        self.__pinned: Dict[str, _Resource] = {}

    def _pin(self, version: str, cls: Type[_R]) -> _R:
        inst = self.__pinned.get(version)
        if inst is None:
            inst = cls(self._client)
            self.__pinned[version] = inst
        return inst  # type: ignore[return-value]


# --------------------------------------------------------------------------
# VectorSnap
# --------------------------------------------------------------------------


class VectorSnapV1(_Resource):
    """IoC reputation enrichment for url, hash, ip, domain (API v1)."""

    _PREFIX = "/v1/ioc/search"

    def url(self, query: str, *, raw_response: bool = False) -> IocUrlScanData:
        return self._client._request(
            f"{self._PREFIX}/url", {"query": query}, IocUrlScanData, raw_response=raw_response
        )

    def hash(self, query: str, *, raw_response: bool = False) -> IocHashScanData:
        return self._client._request(
            f"{self._PREFIX}/hash", {"query": query}, IocHashScanData, raw_response=raw_response
        )

    def ip(self, query: str, *, raw_response: bool = False) -> IocIpScanData:
        return self._client._request(
            f"{self._PREFIX}/ip", {"query": query}, IocIpScanData, raw_response=raw_response
        )

    def domain(self, query: str, *, raw_response: bool = False) -> IocDomainScanData:
        return self._client._request(
            f"{self._PREFIX}/domain", {"query": query}, IocDomainScanData, raw_response=raw_response
        )


class VectorSnap(_VersionedNamespace, VectorSnapV1):
    """IoC reputation enrichment. Direct calls use the latest API version;
    pin to a specific version via :attr:`v1`."""

    @property
    def v1(self) -> VectorSnapV1:
        return self._pin("v1", VectorSnapV1)


# --------------------------------------------------------------------------
# PulseSnap
# --------------------------------------------------------------------------


class PulseSnapV1(_Resource):
    """Threat-intelligence pulse enrichment for url, hash, ip, domain (API v1)."""

    _PREFIX = "/v1/pulse-snap/scan"

    def url(self, query: str, *, raw_response: bool = False) -> PulseUrlScanData:
        return self._client._request(
            f"{self._PREFIX}/url", {"query": query}, PulseUrlScanData, raw_response=raw_response
        )

    def hash(self, query: str, *, raw_response: bool = False) -> PulseHashScanData:
        return self._client._request(
            f"{self._PREFIX}/hash", {"query": query}, PulseHashScanData, raw_response=raw_response
        )

    def ip(self, query: str, *, raw_response: bool = False) -> PulseIpScanData:
        return self._client._request(
            f"{self._PREFIX}/ip", {"query": query}, PulseIpScanData, raw_response=raw_response
        )

    def domain(self, query: str, *, raw_response: bool = False) -> PulseDomainScanData:
        return self._client._request(
            f"{self._PREFIX}/domain", {"query": query}, PulseDomainScanData, raw_response=raw_response
        )


class PulseSnap(_VersionedNamespace, PulseSnapV1):
    """Threat-intelligence pulse enrichment. Direct calls use the latest API
    version; pin to a specific version via :attr:`v1`."""

    @property
    def v1(self) -> PulseSnapV1:
        return self._pin("v1", PulseSnapV1)


# --------------------------------------------------------------------------
# SubdoSnap
# --------------------------------------------------------------------------


class SubdoSnapV1(_Resource):
    """Subdomain enumeration for a domain, paginated (API v1)."""

    _PREFIX = "/v1/subdo-snap"

    def scan(
        self, query: str, *, cursor: Optional[str] = None, raw_response: bool = False
    ) -> SubdoSnapScanData:
        """Fetch one page of subdomains. Pass ``cursor`` to page; see
        :meth:`scan_iter` to stream every subdomain automatically."""
        params: Dict[str, Any] = {"query": query}
        if cursor:
            params["cursor"] = cursor
        return self._client._request(
            f"{self._PREFIX}/scan", params, SubdoSnapScanData, raw_response=raw_response
        )

    def scan_iter(self, query: str) -> Iterator[Any]:
        """Yield every subdomain across all pages, following the cursor for you."""
        cursor: Optional[str] = None
        while True:
            page = self.scan(query, cursor=cursor)
            for subdomain in page.subdomains or []:
                yield subdomain
            cursor = page.cursor
            if not cursor:
                break


class SubdoSnap(_VersionedNamespace, SubdoSnapV1):
    """Subdomain enumeration. Direct calls use the latest API version; pin to a
    specific version via :attr:`v1`."""

    @property
    def v1(self) -> SubdoSnapV1:
        return self._pin("v1", SubdoSnapV1)

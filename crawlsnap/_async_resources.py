"""Async mirror of :mod:`crawlsnap._resources`.

Identical surface and versioning semantics (version is data; unpinned calls use
the stable default; ``vN`` accessors pin one product) — only the methods are
awaitable and ``scan_iter`` is an async generator. See ``_resources.py`` for the
versioning rationale and the "adding a new API version" recipe.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Optional, overload

from typing_extensions import Literal

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
    from ._async_client import AsyncCrawlSnap
    from ._base import RawResponse


class _AsyncResource:
    """Base for one data product on the async client, pinned to one version."""

    _DEFAULT_VERSION = "v1"
    _VERSIONS = ("v1",)

    def __init__(self, client: "AsyncCrawlSnap", version: Optional[str] = None) -> None:
        self._client = client
        self._version = version or self._DEFAULT_VERSION
        self._pins: Dict[str, "_AsyncResource"] = {}

    def _pinned(self, version: str) -> Any:
        inst = self._pins.get(version)
        if inst is None:
            inst = type(self)(self._client, version=version)
            self._pins[version] = inst
        return inst


# --------------------------------------------------------------------------
# VectorSnap
# --------------------------------------------------------------------------


class AsyncVectorSnap(_AsyncResource):
    """IoC reputation enrichment for url / hash / ip / domain (awaitable)."""

    @property
    def v1(self) -> "AsyncVectorSnap":
        return self._pinned("v1")

    @overload
    async def url(self, query: str, *, raw_response: Literal[False] = False) -> IocUrlScanData: ...
    @overload
    async def url(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def url(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/ioc/search/url", {"query": query}, IocUrlScanData, raw_response=raw_response
        )

    @overload
    async def hash(self, query: str, *, raw_response: Literal[False] = False) -> IocHashScanData: ...
    @overload
    async def hash(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def hash(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/ioc/search/hash", {"query": query}, IocHashScanData, raw_response=raw_response
        )

    @overload
    async def ip(self, query: str, *, raw_response: Literal[False] = False) -> IocIpScanData: ...
    @overload
    async def ip(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def ip(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/ioc/search/ip", {"query": query}, IocIpScanData, raw_response=raw_response
        )

    @overload
    async def domain(self, query: str, *, raw_response: Literal[False] = False) -> IocDomainScanData: ...
    @overload
    async def domain(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def domain(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/ioc/search/domain", {"query": query}, IocDomainScanData, raw_response=raw_response
        )


# --------------------------------------------------------------------------
# PulseSnap
# --------------------------------------------------------------------------


class AsyncPulseSnap(_AsyncResource):
    """Threat-intelligence pulse enrichment for url / hash / ip / domain (awaitable)."""

    @property
    def v1(self) -> "AsyncPulseSnap":
        return self._pinned("v1")

    @overload
    async def url(self, query: str, *, raw_response: Literal[False] = False) -> PulseUrlScanData: ...
    @overload
    async def url(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def url(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/pulse-snap/scan/url", {"query": query}, PulseUrlScanData, raw_response=raw_response
        )

    @overload
    async def hash(self, query: str, *, raw_response: Literal[False] = False) -> PulseHashScanData: ...
    @overload
    async def hash(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def hash(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/pulse-snap/scan/hash", {"query": query}, PulseHashScanData, raw_response=raw_response
        )

    @overload
    async def ip(self, query: str, *, raw_response: Literal[False] = False) -> PulseIpScanData: ...
    @overload
    async def ip(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def ip(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/pulse-snap/scan/ip", {"query": query}, PulseIpScanData, raw_response=raw_response
        )

    @overload
    async def domain(self, query: str, *, raw_response: Literal[False] = False) -> PulseDomainScanData: ...
    @overload
    async def domain(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def domain(self, query: str, *, raw_response: bool = False) -> Any:
        return await self._client._request(
            f"/{self._version}/pulse-snap/scan/domain", {"query": query}, PulseDomainScanData, raw_response=raw_response
        )


# --------------------------------------------------------------------------
# SubdoSnap
# --------------------------------------------------------------------------


class AsyncSubdoSnap(_AsyncResource):
    """Subdomain enumeration for a domain, paginated (awaitable)."""

    @property
    def v1(self) -> "AsyncSubdoSnap":
        return self._pinned("v1")

    @overload
    async def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: Literal[False] = False) -> SubdoSnapScanData: ...
    @overload
    async def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: Literal[True]) -> "RawResponse": ...
    async def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: bool = False) -> Any:
        """Fetch one page of subdomains. Pass ``cursor`` to page; see
        :meth:`scan_iter` to stream every subdomain automatically."""
        params: Dict[str, Any] = {"query": query}
        if cursor:
            params["cursor"] = cursor
        return await self._client._request(
            f"/{self._version}/subdo-snap/scan", params, SubdoSnapScanData, raw_response=raw_response
        )

    async def scan_iter(self, query: str) -> AsyncIterator[Any]:
        """Yield every subdomain across all pages, following the cursor for you.

        Use with ``async for``::

            async for subdomain in client.subdo_snap.scan_iter("example.com"):
                ...
        """
        cursor: Optional[str] = None
        while True:
            page = await self.scan(query, cursor=cursor)
            for subdomain in page.subdomains or []:
                yield subdomain
            cursor = page.cursor
            if not cursor:
                break

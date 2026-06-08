"""Resource groups exposed on the client: ``vector_snap``, ``pulse_snap``,
``subdo_snap``. Each method submits one indicator and returns the typed
enrichment payload (the unwrapped ``data``), or raises a typed exception.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional

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


class _Resource:
    def __init__(self, client: "CrawlSnap") -> None:
        self._client = client


class VectorSnap(_Resource):
    """IoC reputation enrichment for url, hash, ip, domain."""

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


class PulseSnap(_Resource):
    """Threat-intelligence pulse enrichment for url, hash, ip, domain."""

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


class SubdoSnap(_Resource):
    """Subdomain enumeration for a domain (paginated)."""

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

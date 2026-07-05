"""Resource groups exposed on the client: ``vector_snap``, ``pulse_snap``,
``subdo_snap``, ``sport_snap``. Each method submits one lookup and returns the
typed payload (the unwrapped ``data``), or raises a typed exception.

Per-API versioning (version is data, not a class hierarchy)
-----------------------------------------------------------
Every CrawlSnap data product is versioned independently, and the version is
carried as a value on the resource (``self._version``), interpolated into the
request path — not encoded as a separate class per version. A direct call uses
that product's **stable default** version::

    client.vector_snap.ip("8.8.8.8")          # default version (stable)

The default is pinned per SDK release via ``_DEFAULT_VERSION`` and never moves
on its own: upgrading the SDK does not silently retarget your calls at a newer
API version. Opt into a specific version explicitly with a version accessor,
which scopes to *one* product and leaves the others untouched::

    client.vector_snap.v1.ip("8.8.8.8")       # explicitly VectorSnap v1
    client.pulse_snap.url("https://x.com")     # unaffected — PulseSnap default

Adding a new API version (e.g. VectorSnap v2)
---------------------------------------------
1. Add ``"v2"`` to the product's ``_VERSIONS`` and a ``v2`` accessor.
2. Regenerate the typed models from the v2 contract.
3. When ready to make v2 the default for unpinned callers, bump
   ``_DEFAULT_VERSION`` to ``"v2"`` in a deliberate SDK release (changelog +
   version bump) — never as a silent side effect of an unrelated upgrade.
"""

from __future__ import annotations

import datetime as _dt
from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, Union, overload
from urllib.parse import quote

from typing_extensions import Literal

from crawlsnap.models.channel_data import ChannelData
from crawlsnap.models.channel_schedule_data import ChannelScheduleData
from crawlsnap.models.country_channels_data import CountryChannelsData
from crawlsnap.models.daily_schedule_data import DailyScheduleData
from crawlsnap.models.ioc_domain_scan_data import IocDomainScanData
from crawlsnap.models.ioc_hash_scan_data import IocHashScanData
from crawlsnap.models.ioc_ip_scan_data import IocIpScanData
from crawlsnap.models.ioc_url_scan_data import IocUrlScanData
from crawlsnap.models.match_data import MatchData
from crawlsnap.models.pulse_domain_scan_data import PulseDomainScanData
from crawlsnap.models.pulse_hash_scan_data import PulseHashScanData
from crawlsnap.models.pulse_ip_scan_data import PulseIpScanData
from crawlsnap.models.pulse_url_scan_data import PulseUrlScanData
from crawlsnap.models.subdo_snap_scan_data import SubdoSnapScanData

if TYPE_CHECKING:
    from ._base import RawResponse
    from ._client import CrawlSnap


class _Resource:
    """Base for a single data product, pinned to one API version.

    The version is a value, not a subtype. A direct call uses
    :data:`_DEFAULT_VERSION` (stable, bumped only by a deliberate SDK release);
    a ``vN`` accessor returns a lazily-cached instance pinned to that version.
    """

    #: Stable default API version. Unpinned calls use this; it does not change
    #: unless the SDK deliberately bumps it in a release.
    _DEFAULT_VERSION = "v1"
    #: API versions this SDK build can talk to.
    _VERSIONS = ("v1",)

    def __init__(self, client: "CrawlSnap", version: Optional[str] = None) -> None:
        self._client = client
        self._version = version or self._DEFAULT_VERSION
        self._pins: Dict[str, "_Resource"] = {}

    def _pinned(self, version: str) -> Any:
        inst = self._pins.get(version)
        if inst is None:
            inst = type(self)(self._client, version=version)
            self._pins[version] = inst
        return inst


# --------------------------------------------------------------------------
# VectorSnap
# --------------------------------------------------------------------------


class VectorSnap(_Resource):
    """IoC reputation enrichment for url / hash / ip / domain.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "VectorSnap":
        return self._pinned("v1")

    @overload
    def url(self, query: str, *, raw_response: Literal[False] = False) -> IocUrlScanData: ...
    @overload
    def url(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def url(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/ioc/search/url", {"query": query}, IocUrlScanData, raw_response=raw_response
        )

    @overload
    def hash(self, query: str, *, raw_response: Literal[False] = False) -> IocHashScanData: ...
    @overload
    def hash(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def hash(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/ioc/search/hash", {"query": query}, IocHashScanData, raw_response=raw_response
        )

    @overload
    def ip(self, query: str, *, raw_response: Literal[False] = False) -> IocIpScanData: ...
    @overload
    def ip(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def ip(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/ioc/search/ip", {"query": query}, IocIpScanData, raw_response=raw_response
        )

    @overload
    def domain(self, query: str, *, raw_response: Literal[False] = False) -> IocDomainScanData: ...
    @overload
    def domain(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def domain(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/ioc/search/domain", {"query": query}, IocDomainScanData, raw_response=raw_response
        )


# --------------------------------------------------------------------------
# PulseSnap
# --------------------------------------------------------------------------


class PulseSnap(_Resource):
    """Threat-intelligence pulse enrichment for url / hash / ip / domain.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "PulseSnap":
        return self._pinned("v1")

    @overload
    def url(self, query: str, *, raw_response: Literal[False] = False) -> PulseUrlScanData: ...
    @overload
    def url(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def url(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/pulse-snap/scan/url", {"query": query}, PulseUrlScanData, raw_response=raw_response
        )

    @overload
    def hash(self, query: str, *, raw_response: Literal[False] = False) -> PulseHashScanData: ...
    @overload
    def hash(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def hash(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/pulse-snap/scan/hash", {"query": query}, PulseHashScanData, raw_response=raw_response
        )

    @overload
    def ip(self, query: str, *, raw_response: Literal[False] = False) -> PulseIpScanData: ...
    @overload
    def ip(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def ip(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/pulse-snap/scan/ip", {"query": query}, PulseIpScanData, raw_response=raw_response
        )

    @overload
    def domain(self, query: str, *, raw_response: Literal[False] = False) -> PulseDomainScanData: ...
    @overload
    def domain(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def domain(self, query: str, *, raw_response: bool = False) -> Any:
        return self._client._request(
            f"/{self._version}/pulse-snap/scan/domain", {"query": query}, PulseDomainScanData, raw_response=raw_response
        )


# --------------------------------------------------------------------------
# SubdoSnap
# --------------------------------------------------------------------------


class SubdoSnap(_Resource):
    """Subdomain enumeration for a domain, paginated.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "SubdoSnap":
        return self._pinned("v1")

    @overload
    def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: Literal[False] = False) -> SubdoSnapScanData: ...
    @overload
    def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: Literal[True]) -> "RawResponse": ...
    def scan(self, query: str, *, cursor: Optional[str] = None, raw_response: bool = False) -> Any:
        """Fetch one page of subdomains. Pass ``cursor`` to page; see
        :meth:`scan_iter` to stream every subdomain automatically."""
        params: Dict[str, Any] = {"query": query}
        if cursor:
            params["cursor"] = cursor
        return self._client._request(
            f"/{self._version}/subdo-snap/scan", params, SubdoSnapScanData, raw_response=raw_response
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


# --------------------------------------------------------------------------
# SportSnap
# --------------------------------------------------------------------------


def _format_date(date: Union[str, "_dt.date"]) -> str:
    """Render a schedule date as ``YYYY-MM-DD`` (accepts str or datetime.date)."""
    if isinstance(date, _dt.date):
        return date.isoformat()
    return date


class SportSnap(_Resource):
    """Live football (soccer) TV listings: channels, broadcast schedules,
    match details with per-country coverage, and daily schedules.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "SportSnap":
        return self._pinned("v1")

    @overload
    def channel(self, slug: str, *, raw_response: Literal[False] = False) -> ChannelData: ...
    @overload
    def channel(self, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def channel(self, slug: str, *, raw_response: bool = False) -> Any:
        """TV channel metadata and competition broadcast rights."""
        return self._client._request(
            f"/{self._version}/sport-snap/channels/{quote(slug, safe='')}",
            {},
            ChannelData,
            raw_response=raw_response,
        )

    @overload
    def channel_schedule(self, slug: str, *, raw_response: Literal[False] = False) -> ChannelScheduleData: ...
    @overload
    def channel_schedule(self, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def channel_schedule(self, slug: str, *, raw_response: bool = False) -> Any:
        """Upcoming broadcast listings for a channel; ``entries`` may be empty."""
        return self._client._request(
            f"/{self._version}/sport-snap/channels/{quote(slug, safe='')}/schedule",
            {},
            ChannelScheduleData,
            raw_response=raw_response,
        )

    @overload
    def match(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match(self, id: int, *, raw_response: bool = False) -> Any:
        """Match details, per-country broadcast coverage, and result data.

        ``status`` discriminates the payload: ``scheduled`` carries meta +
        broadcasts only; ``live``/``finished`` add score, events, statistics,
        and lineups as available."""
        return self._client._request(
            f"/{self._version}/sport-snap/matches/{int(id)}",
            {},
            MatchData,
            raw_response=raw_response,
        )

    @overload
    def country_channels(self, country: str, *, raw_response: Literal[False] = False) -> CountryChannelsData: ...
    @overload
    def country_channels(self, country: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def country_channels(self, country: str, *, raw_response: bool = False) -> Any:
        """TV channels known for a country (slugified name, e.g. ``turkey``)."""
        return self._client._request(
            f"/{self._version}/sport-snap/countries/{quote(country, safe='')}/channels",
            {},
            CountryChannelsData,
            raw_response=raw_response,
        )

    @overload
    def daily_schedule(self, date: Union[str, "_dt.date"], *, raw_response: Literal[False] = False) -> DailyScheduleData: ...
    @overload
    def daily_schedule(self, date: Union[str, "_dt.date"], *, raw_response: Literal[True]) -> "RawResponse": ...
    def daily_schedule(self, date: Union[str, "_dt.date"], *, raw_response: bool = False) -> Any:
        """Daily broadcast schedule grouped by competition.

        Accepts ``YYYY-MM-DD`` or a :class:`datetime.date`."""
        return self._client._request(
            f"/{self._version}/sport-snap/schedules/{quote(_format_date(date), safe='')}",
            {},
            DailyScheduleData,
            raw_response=raw_response,
        )

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

from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, overload
from urllib.parse import quote

from typing_extensions import Literal

from crawlsnap.models.all_teams_data import AllTeamsData
from crawlsnap.models.channel_info_data import ChannelInfoData
from crawlsnap.models.channel_repeats_data import ChannelRepeatsData
from crawlsnap.models.channels_data import ChannelsData
from crawlsnap.models.competition_detail_data import CompetitionDetailData
from crawlsnap.models.competition_tables_data import CompetitionTablesData
from crawlsnap.models.competition_tv_rights_data import CompetitionTvRightsData
from crawlsnap.models.competition_twitter_data import CompetitionTwitterData
from crawlsnap.models.competitions_data import CompetitionsData
from crawlsnap.models.ioc_domain_scan_data import IocDomainScanData
from crawlsnap.models.ioc_hash_scan_data import IocHashScanData
from crawlsnap.models.ioc_ip_scan_data import IocIpScanData
from crawlsnap.models.ioc_url_scan_data import IocUrlScanData
from crawlsnap.models.livescores_data import LivescoresData
from crawlsnap.models.match_data import MatchData
from crawlsnap.models.matches_data import MatchesData
from crawlsnap.models.news_detail_data import NewsDetailData
from crawlsnap.models.news_list_data import NewsListData
from crawlsnap.models.player_data import PlayerData
from crawlsnap.models.popular_teams_data import PopularTeamsData
from crawlsnap.models.pulse_domain_scan_data import PulseDomainScanData
from crawlsnap.models.pulse_hash_scan_data import PulseHashScanData
from crawlsnap.models.pulse_ip_scan_data import PulseIpScanData
from crawlsnap.models.pulse_url_scan_data import PulseUrlScanData
from crawlsnap.models.search_data import SearchData
from crawlsnap.models.subdo_snap_scan_data import SubdoSnapScanData
from crawlsnap.models.team_detail_data import TeamDetailData

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


def _iso_params(iso_code: str) -> Dict[str, Any]:
    """Query values carrying ``iso_code`` only when it is non-empty. ``iso_code``
    is a two-letter region code that resolves region-specific broadcast
    channels; pass ``""`` to use the server default."""
    return {"iso_code": iso_code} if iso_code else {}


def _start_params(start: int) -> Dict[str, Any]:
    """Query values carrying ``start`` only when it is > 0 (``start=0`` is the
    server-default first page)."""
    return {"start": start} if start and start > 0 else {}


def _seg(value: str) -> str:
    """Percent-escape a single path segment."""
    return quote(value, safe="")


class SportSnap(_Resource):
    """Football (soccer) data: live scores, fixtures, single-match views
    (detail, stats, commentary, broadcasts), competitions, national and club
    teams, TV channels and schedules, news, full-text search, and player
    profiles.

    Path segments (competition ``country``/``slug``, team ``country``/``team``,
    player ``slug``/``id``) come from the ``url`` fields in list, search, and
    detail payloads. ``iso_code`` is a two-letter region code that resolves
    region-specific broadcast channels; pass ``""`` to use the server default.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "SportSnap":
        return self._pinned("v1")

    @property
    def _base(self) -> str:
        return f"/{self._version}/sport-snap"

    # -- Live scores & fixtures -----------------------------------------

    @overload
    def livescores(self, *, raw_response: Literal[False] = False) -> LivescoresData: ...
    @overload
    def livescores(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    def livescores(self, *, raw_response: bool = False) -> Any:
        """Live-score board for every tracked competition: score line, match
        status, and structured in-match events."""
        return self._client._request(f"{self._base}/livescores", {}, LivescoresData, raw_response=raw_response)

    @overload
    def matches(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> MatchesData: ...
    @overload
    def matches(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def matches(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Upcoming/current fixtures grouped by competition, with the broadcast
        channels available in the requested ``iso_code`` region. Pass ``""`` for
        the server-default region."""
        return self._client._request(f"{self._base}/matches", _iso_params(iso_code), MatchesData, raw_response=raw_response)

    @overload
    def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: Literal[False] = False) -> MatchesData: ...
    @overload
    def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: bool = False) -> Any:
        """Extended fixture list: adds per-locale team-name translations and
        omits per-fixture channels. ``timestamp`` is a unix-second watermark for
        incremental fetches (0 returns everything)."""
        params = _iso_params(iso_code)
        if timestamp and timestamp > 0:
            params["timestamp"] = timestamp
        return self._client._request(f"{self._base}/xmatches", params, MatchesData, raw_response=raw_response)

    # -- Single match ---------------------------------------------------

    @overload
    def match(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match(self, id: int, *, raw_response: bool = False) -> Any:
        """Full match view keyed by the numeric match id (``fixture_id`` from
        fixture lists, live scores, or search): teams, kickoff, venue, lineups,
        structured events, statistics, and broadcast channels."""
        return self._client._request(f"{self._base}/match/{int(id)}", {}, MatchData, raw_response=raw_response)

    @overload
    def match_extended(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match_extended(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match_extended(self, id: int, *, raw_response: bool = False) -> Any:
        """Extended match view: adds ``*_translations`` maps for the competition
        and team names."""
        return self._client._request(f"{self._base}/xmatch/{int(id)}", {}, MatchData, raw_response=raw_response)

    @overload
    def match_stats(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match_stats(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match_stats(self, id: int, *, raw_response: bool = False) -> Any:
        """Match view with statistics fields populated when the source provides
        them."""
        return self._client._request(f"{self._base}/match/{int(id)}/stats", {}, MatchData, raw_response=raw_response)

    @overload
    def match_commentaries(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match_commentaries(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match_commentaries(self, id: int, *, raw_response: bool = False) -> Any:
        """Match view with the structured event feed populated when the source
        provides it."""
        return self._client._request(f"{self._base}/match/{int(id)}/commentaries", {}, MatchData, raw_response=raw_response)

    @overload
    def match_channels(self, id: int, iso_code: str = "", *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match_channels(self, id: int, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def match_channels(self, id: int, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Match view with broadcast channels resolved for the requested
        ``iso_code`` region."""
        return self._client._request(f"{self._base}/match/{int(id)}/channels", _iso_params(iso_code), MatchData, raw_response=raw_response)

    @overload
    def match_extra_broadcasts(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    def match_extra_broadcasts(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def match_extra_broadcasts(self, id: int, *, raw_response: bool = False) -> Any:
        """Extended match view carrying additional broadcast options (repeats,
        on-demand listings)."""
        return self._client._request(f"{self._base}/xmatch/{int(id)}/extra_broadcasts", {}, MatchData, raw_response=raw_response)

    # -- Competitions ---------------------------------------------------

    @overload
    def competitions(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> CompetitionsData: ...
    @overload
    def competitions(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def competitions(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Competition catalog: popular competitions, domestic leagues grouped by
        country, international club competitions, and tournaments."""
        return self._client._request(f"{self._base}/competitions", _iso_params(iso_code), CompetitionsData, raw_response=raw_response)

    @overload
    def competition(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionDetailData: ...
    @overload
    def competition(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def competition(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Competition detail: fixtures around the current date, standings, top
        scorers, and broadcast-rights holders. ``country``/``slug`` come from
        ``competition_url`` values in other payloads."""
        return self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}", {}, CompetitionDetailData, raw_response=raw_response)

    @overload
    def competition_tables(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTablesData: ...
    @overload
    def competition_tables(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def competition_tables(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Competition standings, grouped by stage."""
        return self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/tables", {}, CompetitionTablesData, raw_response=raw_response)

    @overload
    def competition_tv_rights(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTvRightsData: ...
    @overload
    def competition_tv_rights(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def competition_tv_rights(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Channels holding broadcast rights for the competition."""
        return self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/tv_rights", {}, CompetitionTvRightsData, raw_response=raw_response)

    @overload
    def competition_twitter(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTwitterData: ...
    @overload
    def competition_twitter(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def competition_twitter(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Social feed items for the competition (often empty)."""
        return self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/twitter", {}, CompetitionTwitterData, raw_response=raw_response)

    # -- Teams ----------------------------------------------------------

    @overload
    def popular_teams(self, *, raw_response: Literal[False] = False) -> PopularTeamsData: ...
    @overload
    def popular_teams(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    def popular_teams(self, *, raw_response: bool = False) -> Any:
        """Popular-teams list."""
        return self._client._request(f"{self._base}/teams/popular", {}, PopularTeamsData, raw_response=raw_response)

    @overload
    def all_teams(self, *, raw_response: Literal[False] = False) -> AllTeamsData: ...
    @overload
    def all_teams(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    def all_teams(self, *, raw_response: bool = False) -> Any:
        """Full national-team catalog: per-country men's and women's team names
        with the slugs used by :meth:`national_team`."""
        return self._client._request(f"{self._base}/teams/all", {}, AllTeamsData, raw_response=raw_response)

    @overload
    def national_team(self, slug: str, *, raw_response: Literal[False] = False) -> TeamDetailData: ...
    @overload
    def national_team(self, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def national_team(self, slug: str, *, raw_response: bool = False) -> Any:
        """National-team view (profile, squad, competitions, fixtures) for a
        country slug."""
        return self._client._request(f"{self._base}/countries/{_seg(slug)}", {}, TeamDetailData, raw_response=raw_response)

    @overload
    def club_team(self, country: str, team: str, *, raw_response: Literal[False] = False) -> TeamDetailData: ...
    @overload
    def club_team(self, country: str, team: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def club_team(self, country: str, team: str, *, raw_response: bool = False) -> Any:
        """Club view (profile, squad, competitions, fixtures). ``country``/``team``
        come from team ``url`` values in other payloads (e.g. ``spain``/``barcelona``)."""
        return self._client._request(f"{self._base}/teams/{_seg(country)}/{_seg(team)}", {}, TeamDetailData, raw_response=raw_response)

    # -- Channels -------------------------------------------------------

    @overload
    def all_channels(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelsData: ...
    @overload
    def all_channels(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def all_channels(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Full TV channel catalog for the ``iso_code`` region."""
        return self._client._request(f"{self._base}/all_channels", _iso_params(iso_code), ChannelsData, raw_response=raw_response)

    @overload
    def channels(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelsData: ...
    @overload
    def channels(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def channels(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Curated (football-relevant) channel list for the ``iso_code`` region."""
        return self._client._request(f"{self._base}/channels", _iso_params(iso_code), ChannelsData, raw_response=raw_response)

    @overload
    def channel_info(self, slug: str, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelInfoData: ...
    @overload
    def channel_info(self, slug: str, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def channel_info(self, slug: str, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Channel metadata (name, platform, website, coverage) and the channel's
        broadcast rights for a channel slug."""
        return self._client._request(f"{self._base}/channels/{_seg(slug)}/info", _iso_params(iso_code), ChannelInfoData, raw_response=raw_response)

    @overload
    def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelRepeatsData: ...
    @overload
    def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Channel's repeat/upcoming broadcast schedule with paging cursors. An
        empty ``fixtures`` array is a valid result, not an error."""
        return self._client._request(f"{self._base}/channels/{_seg(slug)}/repeat", _iso_params(iso_code), ChannelRepeatsData, raw_response=raw_response)

    # -- News -----------------------------------------------------------

    @overload
    def news(self, start: int = 0, iso_code: str = "", *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    def news(self, start: int = 0, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    def news(self, start: int = 0, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """News feed, paginated via ``start`` (0 for the first page), for the
        ``iso_code`` region."""
        params = _start_params(start)
        if iso_code:
            params["iso_code"] = iso_code
        return self._client._request(f"{self._base}/news", params, NewsListData, raw_response=raw_response)

    @overload
    def news_by_tag(self, tag: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    def news_by_tag(self, tag: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    def news_by_tag(self, tag: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News carrying the given tag (e.g. ``"messi"``, ``"world-cup"``),
        paginated via ``start``."""
        params: Dict[str, Any] = {"tag": tag}
        params.update(_start_params(start))
        return self._client._request(f"{self._base}/news/tags", params, NewsListData, raw_response=raw_response)

    @overload
    def news_article(self, id: int, *, raw_response: Literal[False] = False) -> NewsDetailData: ...
    @overload
    def news_article(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def news_article(self, id: int, *, raw_response: bool = False) -> Any:
        """Single article (body HTML, tags, byline) plus related articles."""
        return self._client._request(f"{self._base}/news/{int(id)}", {}, NewsDetailData, raw_response=raw_response)

    @overload
    def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a competition, paginated via ``start``."""
        return self._client._request(f"{self._base}/news_about/competitions/{_seg(country)}/{_seg(slug)}", _start_params(start), NewsListData, raw_response=raw_response)

    @overload
    def national_team_news(self, slug: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    def national_team_news(self, slug: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    def national_team_news(self, slug: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a national team, paginated via ``start``."""
        return self._client._request(f"{self._base}/news_about/countries/{_seg(slug)}", _start_params(start), NewsListData, raw_response=raw_response)

    @overload
    def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a club team, paginated via ``start``."""
        return self._client._request(f"{self._base}/news_about/teams/{_seg(country)}/{_seg(team)}", _start_params(start), NewsListData, raw_response=raw_response)

    # -- Search ---------------------------------------------------------

    @overload
    def search_all(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def search_all(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def search_all(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search across teams, competitions, matches, and players.
        Result ``url`` values feed the corresponding endpoints of this API."""
        return self._client._request(f"{self._base}/search/all", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    def search_teams(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def search_teams(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def search_teams(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over teams."""
        return self._client._request(f"{self._base}/search/teams", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    def search_competitions(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def search_competitions(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def search_competitions(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over competitions."""
        return self._client._request(f"{self._base}/search/competitions", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    def search_matches(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def search_matches(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def search_matches(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over matches."""
        return self._client._request(f"{self._base}/search/matches", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    def search_players(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def search_players(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    def search_players(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over players. Result ``url`` values carry the
        ``slug``/``id`` segments used by :meth:`player`."""
        return self._client._request(f"{self._base}/search/players", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    def popular_searches(self, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    def popular_searches(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    def popular_searches(self, *, raw_response: bool = False) -> Any:
        """Currently popular search results."""
        return self._client._request(f"{self._base}/search/popular", {}, SearchData, raw_response=raw_response)

    # -- Players --------------------------------------------------------

    @overload
    def player(self, slug: str, id: int, *, raw_response: Literal[False] = False) -> PlayerData: ...
    @overload
    def player(self, slug: str, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    def player(self, slug: str, id: int, *, raw_response: bool = False) -> Any:
        """Player profile, current team, and per-season statistics. The
        ``slug``/``id`` pair comes from player ``url`` values in search results,
        lineups, and squads."""
        return self._client._request(f"{self._base}/player/{_seg(slug)}/{int(id)}", {}, PlayerData, raw_response=raw_response)

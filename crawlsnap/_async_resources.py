"""Async mirror of :mod:`crawlsnap._resources`.

Identical surface and versioning semantics (version is data; unpinned calls use
the stable default; ``vN`` accessors pin one product) — only the methods are
awaitable and ``scan_iter`` is an async generator. See ``_resources.py`` for the
versioning rationale and the "adding a new API version" recipe.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Optional, overload

from typing_extensions import Literal

from ._resources import _iso_params, _seg, _start_params
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


# --------------------------------------------------------------------------
# SportSnap
# --------------------------------------------------------------------------


class AsyncSportSnap(_AsyncResource):
    """Football (soccer) data (awaitable): live scores, fixtures, single-match
    views (detail, stats, commentary, broadcasts), competitions, national and
    club teams, TV channels and schedules, news, full-text search, and player
    profiles.

    Path segments (competition ``country``/``slug``, team ``country``/``team``,
    player ``slug``/``id``) come from the ``url`` fields in list, search, and
    detail payloads. ``iso_code`` is a two-letter region code that resolves
    region-specific broadcast channels; pass ``""`` to use the server default.

    A direct call uses the stable default version; pin explicitly via
    :attr:`v1`."""

    @property
    def v1(self) -> "AsyncSportSnap":
        return self._pinned("v1")

    @property
    def _base(self) -> str:
        return f"/{self._version}/sport-snap"

    # -- Live scores & fixtures -----------------------------------------

    @overload
    async def livescores(self, *, raw_response: Literal[False] = False) -> LivescoresData: ...
    @overload
    async def livescores(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def livescores(self, *, raw_response: bool = False) -> Any:
        """Live-score board for every tracked competition: score line, match
        status, and structured in-match events."""
        return await self._client._request(f"{self._base}/livescores", {}, LivescoresData, raw_response=raw_response)

    @overload
    async def matches(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> MatchesData: ...
    @overload
    async def matches(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def matches(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Upcoming/current fixtures grouped by competition, with the broadcast
        channels available in the requested ``iso_code`` region. Pass ``""`` for
        the server-default region."""
        return await self._client._request(f"{self._base}/matches", _iso_params(iso_code), MatchesData, raw_response=raw_response)

    @overload
    async def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: Literal[False] = False) -> MatchesData: ...
    @overload
    async def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def matches_extended(self, iso_code: str = "", timestamp: int = 0, *, raw_response: bool = False) -> Any:
        """Extended fixture list: adds per-locale team-name translations and
        omits per-fixture channels. ``timestamp`` is a unix-second watermark for
        incremental fetches (0 returns everything)."""
        params = _iso_params(iso_code)
        if timestamp and timestamp > 0:
            params["timestamp"] = timestamp
        return await self._client._request(f"{self._base}/xmatches", params, MatchesData, raw_response=raw_response)

    # -- Single match ---------------------------------------------------

    @overload
    async def match(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match(self, id: int, *, raw_response: bool = False) -> Any:
        """Full match view keyed by the numeric match id (``fixture_id`` from
        fixture lists, live scores, or search): teams, kickoff, venue, lineups,
        structured events, statistics, and broadcast channels."""
        return await self._client._request(f"{self._base}/match/{int(id)}", {}, MatchData, raw_response=raw_response)

    @overload
    async def match_extended(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match_extended(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match_extended(self, id: int, *, raw_response: bool = False) -> Any:
        """Extended match view: adds ``*_translations`` maps for the competition
        and team names."""
        return await self._client._request(f"{self._base}/xmatch/{int(id)}", {}, MatchData, raw_response=raw_response)

    @overload
    async def match_stats(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match_stats(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match_stats(self, id: int, *, raw_response: bool = False) -> Any:
        """Match view with statistics fields populated when the source provides
        them."""
        return await self._client._request(f"{self._base}/match/{int(id)}/stats", {}, MatchData, raw_response=raw_response)

    @overload
    async def match_commentaries(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match_commentaries(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match_commentaries(self, id: int, *, raw_response: bool = False) -> Any:
        """Match view with the structured event feed populated when the source
        provides it."""
        return await self._client._request(f"{self._base}/match/{int(id)}/commentaries", {}, MatchData, raw_response=raw_response)

    @overload
    async def match_channels(self, id: int, iso_code: str = "", *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match_channels(self, id: int, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match_channels(self, id: int, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Match view with broadcast channels resolved for the requested
        ``iso_code`` region."""
        return await self._client._request(f"{self._base}/match/{int(id)}/channels", _iso_params(iso_code), MatchData, raw_response=raw_response)

    @overload
    async def match_extra_broadcasts(self, id: int, *, raw_response: Literal[False] = False) -> MatchData: ...
    @overload
    async def match_extra_broadcasts(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def match_extra_broadcasts(self, id: int, *, raw_response: bool = False) -> Any:
        """Extended match view carrying additional broadcast options (repeats,
        on-demand listings)."""
        return await self._client._request(f"{self._base}/xmatch/{int(id)}/extra_broadcasts", {}, MatchData, raw_response=raw_response)

    # -- Competitions ---------------------------------------------------

    @overload
    async def competitions(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> CompetitionsData: ...
    @overload
    async def competitions(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competitions(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Competition catalog: popular competitions, domestic leagues grouped by
        country, international club competitions, and tournaments."""
        return await self._client._request(f"{self._base}/competitions", _iso_params(iso_code), CompetitionsData, raw_response=raw_response)

    @overload
    async def competition(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionDetailData: ...
    @overload
    async def competition(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competition(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Competition detail: fixtures around the current date, standings, top
        scorers, and broadcast-rights holders. ``country``/``slug`` come from
        ``competition_url`` values in other payloads."""
        return await self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}", {}, CompetitionDetailData, raw_response=raw_response)

    @overload
    async def competition_tables(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTablesData: ...
    @overload
    async def competition_tables(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competition_tables(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Competition standings, grouped by stage."""
        return await self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/tables", {}, CompetitionTablesData, raw_response=raw_response)

    @overload
    async def competition_tv_rights(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTvRightsData: ...
    @overload
    async def competition_tv_rights(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competition_tv_rights(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Channels holding broadcast rights for the competition."""
        return await self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/tv_rights", {}, CompetitionTvRightsData, raw_response=raw_response)

    @overload
    async def competition_twitter(self, country: str, slug: str, *, raw_response: Literal[False] = False) -> CompetitionTwitterData: ...
    @overload
    async def competition_twitter(self, country: str, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competition_twitter(self, country: str, slug: str, *, raw_response: bool = False) -> Any:
        """Social feed items for the competition (often empty)."""
        return await self._client._request(f"{self._base}/competitions/{_seg(country)}/{_seg(slug)}/twitter", {}, CompetitionTwitterData, raw_response=raw_response)

    # -- Teams ----------------------------------------------------------

    @overload
    async def popular_teams(self, *, raw_response: Literal[False] = False) -> PopularTeamsData: ...
    @overload
    async def popular_teams(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def popular_teams(self, *, raw_response: bool = False) -> Any:
        """Popular-teams list."""
        return await self._client._request(f"{self._base}/teams/popular", {}, PopularTeamsData, raw_response=raw_response)

    @overload
    async def all_teams(self, *, raw_response: Literal[False] = False) -> AllTeamsData: ...
    @overload
    async def all_teams(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def all_teams(self, *, raw_response: bool = False) -> Any:
        """Full national-team catalog: per-country men's and women's team names
        with the slugs used by :meth:`national_team`."""
        return await self._client._request(f"{self._base}/teams/all", {}, AllTeamsData, raw_response=raw_response)

    @overload
    async def national_team(self, slug: str, *, raw_response: Literal[False] = False) -> TeamDetailData: ...
    @overload
    async def national_team(self, slug: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def national_team(self, slug: str, *, raw_response: bool = False) -> Any:
        """National-team view (profile, squad, competitions, fixtures) for a
        country slug."""
        return await self._client._request(f"{self._base}/countries/{_seg(slug)}", {}, TeamDetailData, raw_response=raw_response)

    @overload
    async def club_team(self, country: str, team: str, *, raw_response: Literal[False] = False) -> TeamDetailData: ...
    @overload
    async def club_team(self, country: str, team: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def club_team(self, country: str, team: str, *, raw_response: bool = False) -> Any:
        """Club view (profile, squad, competitions, fixtures). ``country``/``team``
        come from team ``url`` values in other payloads (e.g. ``spain``/``barcelona``)."""
        return await self._client._request(f"{self._base}/teams/{_seg(country)}/{_seg(team)}", {}, TeamDetailData, raw_response=raw_response)

    # -- Channels -------------------------------------------------------

    @overload
    async def all_channels(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelsData: ...
    @overload
    async def all_channels(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def all_channels(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Full TV channel catalog for the ``iso_code`` region."""
        return await self._client._request(f"{self._base}/all_channels", _iso_params(iso_code), ChannelsData, raw_response=raw_response)

    @overload
    async def channels(self, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelsData: ...
    @overload
    async def channels(self, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def channels(self, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Curated (football-relevant) channel list for the ``iso_code`` region."""
        return await self._client._request(f"{self._base}/channels", _iso_params(iso_code), ChannelsData, raw_response=raw_response)

    @overload
    async def channel_info(self, slug: str, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelInfoData: ...
    @overload
    async def channel_info(self, slug: str, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def channel_info(self, slug: str, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Channel metadata (name, platform, website, coverage) and the channel's
        broadcast rights for a channel slug."""
        return await self._client._request(f"{self._base}/channels/{_seg(slug)}/info", _iso_params(iso_code), ChannelInfoData, raw_response=raw_response)

    @overload
    async def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: Literal[False] = False) -> ChannelRepeatsData: ...
    @overload
    async def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def channel_repeats(self, slug: str, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """Channel's repeat/upcoming broadcast schedule with paging cursors. An
        empty ``fixtures`` array is a valid result, not an error."""
        return await self._client._request(f"{self._base}/channels/{_seg(slug)}/repeat", _iso_params(iso_code), ChannelRepeatsData, raw_response=raw_response)

    # -- News -----------------------------------------------------------

    @overload
    async def news(self, start: int = 0, iso_code: str = "", *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    async def news(self, start: int = 0, iso_code: str = "", *, raw_response: Literal[True]) -> "RawResponse": ...
    async def news(self, start: int = 0, iso_code: str = "", *, raw_response: bool = False) -> Any:
        """News feed, paginated via ``start`` (0 for the first page), for the
        ``iso_code`` region."""
        params = _start_params(start)
        if iso_code:
            params["iso_code"] = iso_code
        return await self._client._request(f"{self._base}/news", params, NewsListData, raw_response=raw_response)

    @overload
    async def news_by_tag(self, tag: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    async def news_by_tag(self, tag: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def news_by_tag(self, tag: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News carrying the given tag (e.g. ``"messi"``, ``"world-cup"``),
        paginated via ``start``."""
        params: Dict[str, Any] = {"tag": tag}
        params.update(_start_params(start))
        return await self._client._request(f"{self._base}/news/tags", params, NewsListData, raw_response=raw_response)

    @overload
    async def news_article(self, id: int, *, raw_response: Literal[False] = False) -> NewsDetailData: ...
    @overload
    async def news_article(self, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def news_article(self, id: int, *, raw_response: bool = False) -> Any:
        """Single article (body HTML, tags, byline) plus related articles."""
        return await self._client._request(f"{self._base}/news/{int(id)}", {}, NewsDetailData, raw_response=raw_response)

    @overload
    async def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    async def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def competition_news(self, country: str, slug: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a competition, paginated via ``start``."""
        return await self._client._request(f"{self._base}/news_about/competitions/{_seg(country)}/{_seg(slug)}", _start_params(start), NewsListData, raw_response=raw_response)

    @overload
    async def national_team_news(self, slug: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    async def national_team_news(self, slug: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def national_team_news(self, slug: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a national team, paginated via ``start``."""
        return await self._client._request(f"{self._base}/news_about/countries/{_seg(slug)}", _start_params(start), NewsListData, raw_response=raw_response)

    @overload
    async def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: Literal[False] = False) -> NewsListData: ...
    @overload
    async def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def club_team_news(self, country: str, team: str, start: int = 0, *, raw_response: bool = False) -> Any:
        """News about a club team, paginated via ``start``."""
        return await self._client._request(f"{self._base}/news_about/teams/{_seg(country)}/{_seg(team)}", _start_params(start), NewsListData, raw_response=raw_response)

    # -- Search ---------------------------------------------------------

    @overload
    async def search_all(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def search_all(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def search_all(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search across teams, competitions, matches, and players.
        Result ``url`` values feed the corresponding endpoints of this API."""
        return await self._client._request(f"{self._base}/search/all", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    async def search_teams(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def search_teams(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def search_teams(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over teams."""
        return await self._client._request(f"{self._base}/search/teams", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    async def search_competitions(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def search_competitions(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def search_competitions(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over competitions."""
        return await self._client._request(f"{self._base}/search/competitions", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    async def search_matches(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def search_matches(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def search_matches(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over matches."""
        return await self._client._request(f"{self._base}/search/matches", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    async def search_players(self, query: str, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def search_players(self, query: str, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def search_players(self, query: str, *, raw_response: bool = False) -> Any:
        """Full-text search over players. Result ``url`` values carry the
        ``slug``/``id`` segments used by :meth:`player`."""
        return await self._client._request(f"{self._base}/search/players", {"q": query}, SearchData, raw_response=raw_response)

    @overload
    async def popular_searches(self, *, raw_response: Literal[False] = False) -> SearchData: ...
    @overload
    async def popular_searches(self, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def popular_searches(self, *, raw_response: bool = False) -> Any:
        """Currently popular search results."""
        return await self._client._request(f"{self._base}/search/popular", {}, SearchData, raw_response=raw_response)

    # -- Players --------------------------------------------------------

    @overload
    async def player(self, slug: str, id: int, *, raw_response: Literal[False] = False) -> PlayerData: ...
    @overload
    async def player(self, slug: str, id: int, *, raw_response: Literal[True]) -> "RawResponse": ...
    async def player(self, slug: str, id: int, *, raw_response: bool = False) -> Any:
        """Player profile, current team, and per-season statistics. The
        ``slug``/``id`` pair comes from player ``url`` values in search results,
        lineups, and squads."""
        return await self._client._request(f"{self._base}/player/{_seg(slug)}/{int(id)}", {}, PlayerData, raw_response=raw_response)

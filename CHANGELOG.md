# Changelog

All notable changes to the `crawlsnap` Python SDK are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
this package adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
While the SDK is pre-1.0, minor versions may carry breaking changes; those are
always called out under a `Breaking` heading.

Every entry records the `crawlsnap-contracts` version the release was generated
from, so an SDK version can always be traced back to the public API contract.

Releases before 0.8.0 are not listed here; see the
[git history](https://github.com/crawlsnap/crawlsnap-python/commits/main) for those.

## [Unreleased]

## [0.9.0] - 2026-09-08

Contract: `crawlsnap-contracts` v0.12.0

### Added

- **SerpApi** — new `serp_api` resource (sync and async) with a single method,
  `search(query, *, count, page, language, country, safe, time_range, site,
  filetype)`, returning the typed `SerpSearchData`: ranked Google results for
  one result page plus the related searches Google suggests. Each result's
  `url` is the real target URL, already unwrapped from Google's redirector.
  Available as `crawlsnap.serp_api` on the module singleton, `client.serp_api`
  on an explicit client, and `serp_api.v1` for version pinning.

  Refinements left unset are omitted from the request so the API's own defaults
  apply — the SDK does not pin a default the API is free to move.

## [0.8.0] - 2026-09-05

Contract: `crawlsnap-contracts` v0.11.0

### Added

- `sport_snap.channel_repeats()` (sync and async) accepts an optional `cursor`
  keyword that is forwarded verbatim as the `cursor` query parameter. The
  channel repeat schedule is served as ~20-fixture pages with
  `fixtures_next` / `fixtures_prev` cursors; without this, callers were pinned
  to the first page (roughly two days of schedule). The region is always taken
  from `iso_code`, never from the cursor.

### Changed

- Models regenerated from the bundled contract: the cursor fields on the
  channel repeat payload are now documented.

[Unreleased]: https://github.com/crawlsnap/crawlsnap-python/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/crawlsnap/crawlsnap-python/releases/tag/v0.8.0

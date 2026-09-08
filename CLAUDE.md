# crawlsnap-python

Official Python SDK for the CrawlSnap public API. The typed models under
`crawlsnap/models/` are generated from the public OpenAPI contract
(`crawlsnap-contracts`, family `crawlsnap/v1`) via `./scripts/regenerate.sh`;
the client facade around them is hand-written.

## Releases & changelog

`CHANGELOG.md` is the single source of truth for release notes. Every
user-visible change is written into it **in the same commit that makes the
change** — never generated from commit messages afterwards.

- Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 1.1.0.
  Version headings are `## [x.y.z] - YYYY-MM-DD` (ISO date, newest first) and
  the only section headings allowed are `Added`, `Changed`, `Deprecated`,
  `Removed`, `Fixed`, `Security` and `Breaking`.
- Work in progress goes under `## [Unreleased]`. Cutting a release renames that
  heading to the new version plus today's date, adds a fresh empty
  `## [Unreleased]`, and updates the link definitions at the bottom of the file.
- Every released version starts with a `Contract: crawlsnap-contracts vX.Y.Z`
  line, so an SDK version can always be traced back to the API contract it was
  generated from.
- Write for humans: what changed for a caller and why, not which files moved.
- Pre-1.0 the package uses lenient semver — a minor version may break; when it
  does, say so under a `Breaking` heading.
- The `release` workflow copies the tagged section into the GitHub Release body
  (`gh release edit --notes-file`). Never write release notes by hand in the
  GitHub UI: they will be overwritten. A tag with no matching CHANGELOG section
  fails the workflow on purpose.
- PyPI surfaces the changelog through the `Changelog` well-known label in
  `[project.urls]`; keep that URL working. README links must be absolute — PyPI
  does not resolve relative repository links.

Release flow: bump `crawlsnap/_version.py` → update `CHANGELOG.md` → commit →
tag `vX.Y.Z` → push the tag → publish the GitHub Release (empty body is fine).

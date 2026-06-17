# crawlsnap

Official Python SDK for [CrawlSnap](https://crawlsnap.com) — a data intelligence
platform that delivers structured, on-demand data through fast, typed APIs.
Authenticate once and call any CrawlSnap data product, with first-class types,
automatic retries, and pagination built in.

- Idiomatic, fully typed client (httpx + pydantic v2)
- `crawlsnap.init(...)` singleton **or** an explicit `CrawlSnap` client
- Resource namespacing: `crawlsnap.vector_snap.ip(...)`
- Per-API version pinning: stay on `vector_snap.v1` while other products track latest
- Returns typed data; raises typed exceptions — no envelope bookkeeping
- Built-in retries with exponential backoff, configurable timeout, auto-pagination

---

## Installation

```bash
pip install crawlsnap
```

Requires Python 3.8+.

## Authentication

Get an API key (`sk-cs-...`) from your CrawlSnap dashboard. Provide it either
via the environment or explicitly:

```bash
export CRAWLSNAP_API_KEY=sk-cs-...
```

```python
crawlsnap.init()                       # reads CRAWLSNAP_API_KEY
crawlsnap.init(api_key="sk-cs-...")    # or pass it explicitly
```

The key is sent as `Authorization: Bearer sk-cs-...`. Treat it like a password.

## Quick start

```python
import crawlsnap

crawlsnap.init(api_key="sk-cs-...")

ip = crawlsnap.vector_snap.ip("8.8.8.8")
print(ip.reputation, ip.as_owner, ip.country)
```

Each call returns the typed enrichment payload directly, and raises a typed
exception on failure — you never inspect an `is_success` envelope yourself.

## Resources

| Resource | Methods | Returns |
|----------|---------|---------|
| `vector_snap` | `url` · `hash` · `ip` · `domain` | reputation, detections, categories, relationships |
| `pulse_snap`  | `url` · `hash` · `ip` · `domain` | threat-intelligence pulse (and sandbox) summary |
| `subdo_snap`  | `scan` · `scan_iter` | enumerated subdomains (paginated) |

```python
url    = crawlsnap.vector_snap.url("https://example.com")
file   = crawlsnap.vector_snap.hash("44d88612fea8a8f36de82e1278abb02f")
domain = crawlsnap.vector_snap.domain("google.com")

pulse  = crawlsnap.pulse_snap.ip("8.8.8.8")
```

Every method takes the indicator as the first positional argument and accepts
`raw_response=True` (see below).

## API versioning

Each CrawlSnap data product is versioned **independently**. Calling a resource
method directly always targets that product's **latest** API version:

```python
crawlsnap.vector_snap.ip("8.8.8.8")        # latest VectorSnap
```

When a product ships a new API version, you don't have to pin the whole SDK (or
hold back every other product) to keep your current behavior. Pin just the one
you care about via its version namespace — everything else stays on latest:

```python
crawlsnap.vector_snap.v1.ip("8.8.8.8")     # explicitly VectorSnap v1
crawlsnap.pulse_snap.url("https://x.com")  # still latest PulseSnap
```

The same applies on an explicit client (`client.vector_snap.v1.ip(...)`). Pinned
namespaces (`.v1`, and future `.v2`, …) are typed, so your IDE and type checker
see the exact payload shape for that version. Upgrade at your own pace: switch a
call from `.v1` to the default (or `.v2`) when you're ready.

## Error handling

Failures raise a typed exception instead of returning an error envelope:

```python
from crawlsnap import (
    NotFoundError, RateLimitError, QuotaExceededError,
    AuthenticationError, CrawlSnapError,
)

try:
    res = crawlsnap.vector_snap.domain("example.com")
except NotFoundError:
    ...                              # 404 — no data for this indicator
except QuotaExceededError as e:
    print(e.message)                 # 402 — out of credits / monthly quota
except RateLimitError as e:
    print(e.retry_after)             # 429 — daily limit; seconds to wait
except AuthenticationError:
    ...                              # 401 — missing / invalid key
except CrawlSnapError as e:          # base class for every SDK error
    print(e)
```

| HTTP | Exception | Notes |
|------|-----------|-------|
| 400 | `BadRequestError` | invalid indicator |
| 401 | `AuthenticationError` | missing / invalid key |
| 402 | `QuotaExceededError` | out of credits or monthly quota |
| 403 | `SubscriptionInactiveError` | subscription not active |
| 404 | `NotFoundError` | no data for the indicator |
| 429 | `RateLimitError` | daily limit; `.retry_after` (seconds) |
| 5xx | `ServerError` | server / upstream failure |
| — | `APIConnectionError` / `APITimeoutError` | network failure / client timeout |

Every status error carries `.status_code`, `.message`, and `.request_id`
(share the request id with support to speed up debugging).

## Pagination

`subdo_snap` is paginated. Stream every subdomain across all pages — the cursor
is handled for you:

```python
for subdomain in crawlsnap.subdo_snap.scan_iter("example.com"):
    print(subdomain)
```

Or page manually:

```python
page = crawlsnap.subdo_snap.scan("example.com")
while page.cursor:
    page = crawlsnap.subdo_snap.scan("example.com", cursor=page.cursor)
```

## Configuration

The singleton is a thin layer over the `CrawlSnap` client. For multiple keys,
multiple environments, or thread isolation, instantiate it directly:

```python
from crawlsnap import CrawlSnap

client = CrawlSnap(
    api_key="sk-cs-...",
    timeout=30.0,
    max_retries=3,
    base_url="https://api.crawlsnap.com",
)
ip = client.vector_snap.ip("1.1.1.1")
client.close()
```

| Option | Default | Description |
|--------|---------|-------------|
| `api_key` | `$CRAWLSNAP_API_KEY` | Your `sk-cs-` key |
| `base_url` | `$CRAWLSNAP_BASE_URL` or `https://api.crawlsnap.com` | API host override |
| `timeout` | `30.0` | Per-request timeout (seconds) |
| `max_retries` | `2` | Retries for 429 / 5xx / connection errors |

Retries use exponential backoff and honor the `Retry-After` header on 429.

### Raw response

Pass `raw_response=True` to get the full envelope (status, headers, request id)
instead of just the data:

```python
raw = crawlsnap.vector_snap.ip("8.8.8.8", raw_response=True)
print(raw.status_code, raw.request_id, raw.is_success, raw.data)
```

## Development

The typed models under `crawlsnap/models/` are generated from the public
OpenAPI contract; the client facade is hand-written. To refresh the models
after the contract changes:

```bash
./scripts/regenerate.sh        # re-bundles the contract and regenerates models/
```

Run the tests:

```bash
pip install -e ".[dev]"
pytest
```

# crawlsnap

Official Python SDK for the [CrawlSnap](https://crawlsnap.com) threat-intelligence
API — on-demand IoC enrichment for URLs, file hashes, IPv4 addresses, and domains.

## Install

```bash
pip install crawlsnap
```

## Quick start

Initialize once, then call the resources directly:

```python
import crawlsnap

crawlsnap.init(api_key="sk-cs-...")          # or export CRAWLSNAP_API_KEY=sk-cs-...

ip = crawlsnap.vector_scan.ip("8.8.8.8")
print(ip.reputation, ip.as_owner, ip.country)
```

Each call returns the typed enrichment payload directly, and raises a typed
exception on failure — no envelope/`is_success` checks needed.

## The three families

```python
url    = crawlsnap.vector_scan.url("https://example.com")
file   = crawlsnap.vector_scan.hash("44d88612fea8a8f36de82e1278abb02f")
domain = crawlsnap.vector_scan.domain("google.com")

pulse  = crawlsnap.pulse_snap.ip("45.83.122.10")

# subdomain enumeration (paginated)
for subdomain in crawlsnap.subdo_snap.scan_iter("example.com"):
    print(subdomain)
```

| Resource | Methods | Source |
|----------|---------|--------|
| `vector_scan` | `url` · `hash` · `ip` · `domain` | VirusTotal |
| `pulse_snap`  | `url` · `hash` · `ip` · `domain` | AlienVault OTX |
| `subdo_snap`  | `scan` · `scan_iter` | subdomain enumeration |

## Error handling

```python
from crawlsnap import (
    NotFoundError, RateLimitError, QuotaExceededError,
    AuthenticationError, CrawlSnapError,
)

try:
    res = crawlsnap.vector_scan.domain("example.com")
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

| HTTP | Exception |
|------|-----------|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 402 | `QuotaExceededError` |
| 403 | `SubscriptionInactiveError` |
| 404 | `NotFoundError` |
| 429 | `RateLimitError` (`.retry_after`) |
| 5xx | `ServerError` |
| network / timeout | `APIConnectionError` / `APITimeoutError` |

All status errors carry `.status_code`, `.message`, and `.request_id`.

## Advanced — your own client

The singleton is a thin layer over the `CrawlSnap` client. For multiple keys,
multiple environments, or thread isolation, instantiate it directly:

```python
from crawlsnap import CrawlSnap

client = CrawlSnap(
    api_key="sk-cs-...",
    timeout=30.0,
    max_retries=3,          # exponential backoff on 429 / 5xx / connection errors
    base_url="https://api.crawlsnap.com",
)
ip = client.vector_scan.ip("1.1.1.1")
client.close()
```

Retries (429/5xx, honoring `Retry-After`) and a 30s timeout are on by default.

### Raw response

Pass `raw_response=True` to get the full envelope (status, headers, request id):

```python
raw = crawlsnap.vector_scan.ip("8.8.8.8", raw_response=True)
print(raw.status_code, raw.request_id, raw.data)
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

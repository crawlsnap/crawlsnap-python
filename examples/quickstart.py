"""CrawlSnap Python SDK — quickstart.

    export CRAWLSNAP_API_KEY=sk-cs-...
    python examples/quickstart.py
"""

import os

import crawlsnap
from crawlsnap import CrawlSnapError, NotFoundError, QuotaExceededError, RateLimitError

crawlsnap.init(api_key=os.environ["CRAWLSNAP_API_KEY"])

# 1. IP reputation (VirusTotal-derived)
ip = crawlsnap.vector_scan.ip("8.8.8.8")
print(f"8.8.8.8        -> {ip.as_owner} ({ip.country}), reputation {ip.reputation}")

# 2. Domain
domain = crawlsnap.vector_scan.domain("google.com")
print(f"google.com     -> registrar={domain.registrar}, reputation={domain.reputation}")

# 3. File hash (EICAR test file)
sample = crawlsnap.vector_scan.hash("44d88612fea8a8f36de82e1278abb02f")
print(f"eicar hash     -> {sample.meaningful_name} / {sample.type_description}")

# 4. OTX pulse enrichment
pulse = crawlsnap.pulse_snap.ip("8.8.8.8")
print(f"otx pulse      -> {pulse.pulse_detail}")

# 5. Error handling — failures raise typed exceptions
try:
    crawlsnap.vector_scan.domain("nonexistent-xyz.invalid")
except NotFoundError:
    print("lookup miss    -> no data for that indicator")
except QuotaExceededError as e:
    print(f"quota          -> {e.message}")
except RateLimitError as e:
    print(f"rate limited   -> retry in {e.retry_after}s")
except CrawlSnapError as e:
    print(f"error          -> {e}")

# 6. Subdomain enumeration — cursor handled for you
print("subdomains     ->")
for sub in crawlsnap.subdo_snap.scan_iter("example.com"):
    print("                 ", sub)

#!/usr/bin/env bash
# Regenerate this SDK from the public CrawlSnap OpenAPI contract.
#
# Source of truth: ../crawlsnap-contracts/crawlsnap/v1/openapi.yaml — bundled
# into a single self-contained file first (resolves the cross-file $ref into
# ioc-scan). Never hand-edit the generated client; change the contract and
# re-run this script. Custom files are protected via .openapi-generator-ignore.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTRACTS="${CONTRACTS_DIR:-$REPO_ROOT/../crawlsnap-contracts}"
SPEC="$CONTRACTS/dist/crawlsnap-v1.yaml"
VERSION="${PACKAGE_VERSION:-0.1.0}"

# 1. Bundle the contract (inlines the ioc-scan data schemas).
( cd "$CONTRACTS" && make bundle )

# 2. Generate the Python client from the bundle.
npx -y @openapitools/openapi-generator-cli@latest generate \
  -i "$SPEC" \
  -g python \
  -o "$REPO_ROOT" \
  --additional-properties=packageName=crawlsnap,projectName=crawlsnap,packageVersion=${VERSION},hideGenerationTimestamp=true

echo "==> Regenerated crawlsnap Python SDK v${VERSION} from $SPEC"

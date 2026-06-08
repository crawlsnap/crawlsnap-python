#!/usr/bin/env bash
# Refresh the typed models in crawlsnap/models/ from the public OpenAPI contract.
#
# Only the models are generated; the hand-written facade (_client.py,
# _resources.py, __init__.py, _exceptions.py) is never touched. A throwaway
# full client is generated into a temp dir and only its models/ is copied in.
#
# Source of truth: ../crawlsnap-contracts/crawlsnap/v1/openapi.yaml
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONTRACTS="${CONTRACTS_DIR:-$REPO_ROOT/../crawlsnap-contracts}"
SPEC="$CONTRACTS/dist/crawlsnap-v1.yaml"
TMP="$REPO_ROOT/.gen-tmp"
VERSION="${PACKAGE_VERSION:-0.1.0}"

# 1. Bundle the contract (inlines the ioc-scan data schemas).
( cd "$CONTRACTS" && make bundle )

# 2. Generate a throwaway full client.
rm -rf "$TMP"
npx -y @openapitools/openapi-generator-cli@latest generate \
  -i "$SPEC" -g python -o "$TMP" \
  --additional-properties=packageName=crawlsnap,projectName=crawlsnap,packageVersion="${VERSION}",hideGenerationTimestamp=true \
  >/dev/null

# 3. Replace models in place; leave the facade untouched.
rm -rf "$REPO_ROOT/crawlsnap/models"
cp -R "$TMP/crawlsnap/models" "$REPO_ROOT/crawlsnap/models"
rm -rf "$TMP"

echo "==> Refreshed crawlsnap/models from $SPEC (facade left intact)"

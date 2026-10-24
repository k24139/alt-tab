#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/verify_free_source.py
temporary="$(mktemp -d "${TMPDIR:-/tmp}/alttab-free-tests.XXXXXX")"
trap 'rm -rf "$temporary"' EXIT
xcrun swiftc -warnings-as-errors -module-cache-path "$temporary/cache" \
    src/switcher/state/SearchModeResolver.swift \
    src/switcher/search-discovery/SearchDiscoveryPolicy.swift \
    scripts/test_free_features.swift -o "$temporary/free-feature-checks"
"$temporary/free-feature-checks"

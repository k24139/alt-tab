#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! xcodebuild -version >/dev/null 2>&1; then
    echo 'Install full Xcode, then select it with: sudo xcode-select -s /Applications/Xcode.app/Contents/Developer' >&2
    exit 1
fi
python3 scripts/verify_free_source.py
python3 scripts/assets/compile_illustrations.py --check
identity="${ALTTAB_SIGNING_IDENTITY:--}"
architecture="${ALTTAB_ARCHS:-$(uname -m)}"
xcodebuild -project alt-tab-macos.xcodeproj -scheme Release -configuration Release \
    -derivedDataPath DerivedData-Free \
    CURRENT_PROJECT_VERSION=11.10.1 DEVELOPMENT_TEAM= CODE_SIGN_IDENTITY="$identity" \
    CODE_SIGN_STYLE=Manual CODE_SIGN_INJECT_BASE_ENTITLEMENTS=NO \
    OTHER_CODE_SIGN_FLAGS=--timestamp=none ARCHS="$architecture" ONLY_ACTIVE_ARCH=NO \
    build
app="$PWD/DerivedData-Free/Build/Products/Release/AltTab.app"
codesign --verify --deep --strict --verbose=2 "$app"
mkdir -p build
ditto -c -k --sequesterRsrc --keepParent "$app" "$PWD/build/AltTab-Free-macOS.zip"
shasum -a 256 "$PWD/build/AltTab-Free-macOS.zip" > "$PWD/build/AltTab-Free-macOS.zip.sha256"
printf 'Application: %s\nArchive: %s\n' "$app" "$PWD/build/AltTab-Free-macOS.zip"

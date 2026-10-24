# Source verification

Date: October 24, 2026.
Baseline: `c500294bdb01186011a5c64a412b04cef9931bef`, upstream release 11.10.1.
Branch: `free-self-build`.
Host: Apple Silicon macOS, Apple Swift 6.3.3, Command Line Tools selected.

## Passed

- All 199 application Swift source files type check in both Release and Debug conditions, targeting macOS 12, with warnings treated as errors. The check imports the actual vendored ShortcutRecorder, AppCenter, and AppCenterCrashes headers. No replacement app types or entitlement mocks are used. Commands: `python3 scripts/typecheck_free_source.py` and `python3 scripts/typecheck_free_source.py --debug`.
- `bash scripts/test_free_source.sh`: free-build source rules and executable checks against the production search state machine and discovery policy. Covers entering search, re-entering search, search-on-release, Escape behavior, arrow routing, text composition, discovery history, and days 0, 15, 35, 365, and 3650.
- `python3 scripts/verify_free_source.py`: Xcode object references, all build source paths, absence of commercial entry points, permanent direct preference reads, search entry, separate app identity, and absence of Sparkle or updater/activation bundle metadata. The test target retains 145 Swift source files.
- Generated illustration validation: 29 illustrations. Six illustration compiler tests pass.
- All 21 translated app catalogs and the root catalog match the 273 remaining source localization keys. All translated values are nonempty and format placeholders match. The literal-key extraction was cross-checked against the baseline catalog: all 363 original keys matched with no missing or extra keys.
- Project and bundle plist syntax, shell script syntax, and `git diff --check` pass.
- `scripts/build_free.sh` prerequisite handling: stops before compilation and explains how to install/select full Xcode.

## Requires the manual Xcode build

`ai/build.sh` reaches `xcodebuild`, which rejects the active Command Line Tools developer directory. `ai/test.sh` stops at localization extraction since `genstrings` requires full Xcode in this environment. XCTest is also absent from the selected tools. The full XCTest suite, the standard genstrings-based localization check, linking, app signing, packaging, and live app tests have not run.

No `.app` has been built or launched. Source type checking and executable logic checks do not establish macOS integration behavior. Verify the Release app's permissions, window previews, search, extra shortcuts, appearance styles, auto sizing, search-on-release, persistence, login launch, Spaces, fullscreen, and multiple displays after building. Intel and universal execution remain untested.

The build script creates a local signed app, ZIP, and checksum after Xcode is available. It does not notarize or publish the app. The application has no update implementation, update menu, update settings, background update timer, feedback update prompt, or linked Sparkle dependency.

## GitHub application build completed

The Apple Silicon Release application built successfully on GitHub macOS 26.6.2 with Xcode 26.6. `codesign --verify --deep --strict` reports the app valid on disk and satisfying its designated requirement. The ZIP and SHA-256 checksum uploaded successfully. Run: https://github.com/k24139/alt-tab/actions/runs/40115322580 . This supersedes the earlier local build limitation. Live app integration tests and the full XCTest suite remain pending.

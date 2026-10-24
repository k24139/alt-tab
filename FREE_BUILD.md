# AltTab Free self-build

This modified GPL-3.0 fork of Louis Pontoise's AltTab makes all local features available without a license. It has no trial, activation flow, purchase interface, update checks, update notifications, or automatic installation of updates. Upstream author credits and the license remain in the repository and About window.

The app is named `AltTab-Free` and uses the stable bundle identifier `com.k24139.alt-tab-free`. It has separate settings and macOS permission records. It does not read or change the official app's license, Keychain entries, or preferences. To bring existing settings over, export them from the official app and import them through this fork's General settings. Values that the official app already downgraded are not recoverable from a normal settings export. Select those values again in this app.

## Manual build

Install full Xcode and its macOS SDK, launch Xcode once to finish setup and accept its license, and select its developer directory:

```sh
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

From this repository, run:

```sh
bash scripts/build_free.sh
```

The script checks the free-build rules and generated artwork, builds the Release target for your Mac's architecture, signs it for local use, verifies the signature, and creates:

- `DerivedData-Free/Build/Products/Release/AltTab-Free.app`
- `build/AltTab-Free-macOS.zip`
- `build/AltTab-Free-macOS.zip.sha256`

No Apple developer subscription, upstream signing secrets, Node installation, server, or license key is required. Dependencies are vendored. The default signature is ad hoc. It is for personal local use and is not notarized. For a stable certificate signature, set `ALTTAB_SIGNING_IDENTITY` to an existing code-signing identity and keep using that identity on later builds. Ad hoc rebuilds can require granting macOS permissions again. The script does not create certificates or change Keychain trust.

For a universal build, run:

```sh
ALTTAB_ARCHS='arm64 x86_64' bash scripts/build_free.sh
```

That path still requires verification on Intel hardware.

Copy the app to `/Applications`, launch it through Finder, and grant Accessibility and Screen Recording permissions. Quit official AltTab before running both apps with the same shortcuts. macOS security prompts and permission guidance remain part of normal operation.

## Verification with Xcode

These source checks also run with Command Line Tools:

```sh
bash scripts/test_free_source.sh
python3 scripts/typecheck_free_source.py
python3 scripts/typecheck_free_source.py --debug
```

With full Xcode, run the repository's unit tests and app checks:

```sh
bash ai/test.sh
bash ai/build.sh
```

Debug and Release use ad hoc signing by default. A developer can override it in the ignored `config/local.xcconfig`. The fork identity comes from `config/base.xcconfig`. Keep that identity unchanged in local overrides.

Before treating the app as verified, test the actual Release bundle: first launch, search and locked search, extra shortcuts, all three appearance styles, automatic sizing, search on shortcut release, settings persistence, login launch, window actions, Spaces, fullscreen, and multiple displays. Repeat offline and after relaunch. No date or trial state is read to grant access. There is no updater linked to the app.

## Changes from upstream

Baseline commit: `c500294bdb01186011a5c64a412b04cef9931bef`.

Removed the licensing implementation, machine fingerprinting, license Keychain operations, license cookies, trial scheduler, feature downgrades, checkout attribution, promotional surfaces, and their dedicated visual QA commands and tests. Removed the Sparkle app dependency, updater helpers build phase, bundle updater metadata, update controls, and the feedback update preflight. Ordinary onboarding, search, shortcuts, appearance controls, feedback, and core window switching remain.

The fork's workflow checks source rules and artwork only. Builds and releases are manual. It never publishes an upstream appcast or invokes the upstream release pipeline.

See `VERIFICATION.md` for the checks completed before the manual build.

## Build on GitHub

Open Actions, select **Build AltTab Free**, choose **Run workflow** on `master`, and run it. After success, download **AltTab-Free-macOS** under Artifacts. Extract the artifact, then the application ZIP inside it. Artifacts expire after seven days. No Xcode installation on your Mac is needed.

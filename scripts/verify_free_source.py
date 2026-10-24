#!/usr/bin/env python3
"""Guard the permanent free build and validate Xcode references without building an app."""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def project_sources():
    project = json.loads(subprocess.check_output([
        'plutil', '-convert', 'json', '-o', '-',
        str(ROOT / 'alt-tab-macos.xcodeproj/project.pbxproj')]))
    objects = project['objects']
    paths = {}

    def visit(identifier, parent):
        item = objects[identifier]
        base = ROOT if item.get('sourceTree') == 'SOURCE_ROOT' else parent
        path = base / item.get('path', '')
        if item['isa'] == 'PBXFileReference':
            paths[identifier] = path
        for child in item.get('children', []):
            visit(child, path)

    visit(objects[project['rootObject']]['mainGroup'], ROOT)

    def check_references(value):
        if isinstance(value, dict):
            for child in value.values():
                check_references(child)
        elif isinstance(value, list):
            for child in value:
                check_references(child)
        elif isinstance(value, str) and re.fullmatch(r'[A-Z0-9]{24}', value):
            assert value in objects, f'Dangling Xcode reference: {value}'

    check_references(project)
    targets = {}
    for item in objects.values():
        if item['isa'] != 'PBXNativeTarget':
            continue
        sources = []
        for phase_id in item['buildPhases']:
            phase = objects[phase_id]
            if phase['isa'] != 'PBXSourcesBuildPhase':
                continue
            for entry in phase['files']:
                file_id = objects[entry]['fileRef']
                path = paths.get(file_id, ROOT / objects[file_id].get('path', ''))
                assert path.is_file(), f'Missing build source: {path}'
                if path.suffix == '.swift':
                    sources.append(path)
        targets[item['name']] = sources
    return targets


def verify():
    targets = project_sources()
    banned = re.compile(r'\b(?:LicenseManager|LicenseState|ProFeature|ProTransitionManager|'
                        r'ProTransitionState|ProPromptHost|ProPromptWindow|ProBadgeView|'
                        r'UpgradeTab|CheckoutOrigin|MachineFingerprint|RemoteLicenseClient|'
                        r'SystemKeychain|SPUStandardUpdaterController|Sparkle|checkForUpdates|'
                        r'checkForUpdateInformation|SUEnableAutomaticChecks)\b')
    for path in targets['alt-tab-macos']:
        text = re.sub(r'(?m)^\s*//[^\n]*', '', path.read_text())
        assert not banned.search(text), f'Commercial or updater entry point: {path}'
    import plistlib
    info = plistlib.loads((ROOT / 'Info.plist').read_bytes())
    assert not any(key.startswith('SU') for key in info), 'Updater metadata remains'
    assert 'CFBundleURLTypes' not in info, 'Activation URL scheme remains'
    project = (ROOT / 'alt-tab-macos.xcodeproj/project.pbxproj').read_text()
    assert 'Sparkle' not in project, 'Updater is still an Xcode dependency'
    config = (ROOT / 'config/base.xcconfig').read_text()
    assert 'PRODUCT_BUNDLE_IDENTIFIER = com.k24139.alt-tab-free' in config
    assert 'PRODUCT_NAME = AltTab-Free' in config
    preferences = (ROOT / 'src/preferences/Preferences.swift').read_text()
    assert 'ProGatedPreferences' not in preferences
    for name in ['appearanceStyle', 'appearanceSize', 'shortcutStyle']:
        assert re.search(r'static var ' + name + r':[^\n]+CachedUserDefaults.macroPref', preferences)
    assert 'SearchModeResolver.enableEditing(mode: searchMode)' in (ROOT / 'src/switcher/main-window/TilesView.swift').read_text()
    for path in targets['alt-tab-macos']:
        assert 'attemptUse()' not in path.read_text(), f'Runtime feature gate: {path}'
    print('Free-build rules and Xcode source references passed:',
          len(targets['alt-tab-macos']), 'app Swift files,', len(targets['unit-tests']), 'test-target Swift files')


if __name__ == '__main__':
    try:
        verify()
    except (AssertionError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

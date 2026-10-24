#!/usr/bin/env python3
"""Type check the app using CLT and real vendored headers. Does not link or build an app."""
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from verify_free_source import ROOT, project_sources, verify

verify()
with tempfile.TemporaryDirectory(prefix='alttab-typecheck-') as temporary:
    folder = Path(temporary)
    modules = {
        'ShortcutRecorder': ROOT / 'vendor/ShortcutRecorder/Sources/ShortcutRecorder/include',
        'AppCenter': ROOT / 'vendor/AppCenter/Sources/AppCenter/include',
        'AppCenterCrashes': ROOT / 'vendor/AppCenter/Sources/AppCenterCrashes/include',
    }
    arguments = ['xcrun', 'swiftc', '-typecheck', '-swift-version', '5', '-warnings-as-errors',
                 '-target', platform.machine() + '-apple-macosx12.0', '-module-name', 'AltTabFree',
                 '-module-cache-path', str(folder / 'cache'), '-import-objc-header',
                 str(ROOT / 'alt-tab-macos-Bridging-Header.h'), '-I', str(ROOT / 'src/vendors')]
    for name, headers in modules.items():
        modulemap = folder / (name + '.modulemap')
        modulemap.write_text('module ' + name + ' { umbrella ' + json.dumps(str(headers)) +
                             '\n export *\n module * { export * }\n}\n')
        arguments += ['-Xcc', '-fmodule-map-file=' + str(modulemap), '-I', str(headers)]
    if '--debug' in sys.argv:
        arguments += ['-D', 'DEBUG']
    arguments += [str(path) for path in project_sources()['alt-tab-macos']]
    subprocess.run(arguments, cwd=ROOT, check=True)
    print(('Debug' if '--debug' in sys.argv else 'Release') + ' app source type checking passed')

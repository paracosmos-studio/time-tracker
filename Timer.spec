# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources/close.svg', 'resources'),
        ('resources/dropdown.svg', 'resources'),
        ('resources/fullscreen.svg', 'resources'),
        ('resources/icon.icns', 'resources'),
        ('resources/minimize.svg', 'resources'),
        ('resources/fonts/satoshi_bold.otf', 'resources/fonts'),
        ('resources/fonts/satoshi_medium.otf', 'resources/fonts'),
        ('resources/fonts/satoshi_regular.otf', 'resources/fonts'),
        ('resources/fonts/license.txt', 'resources/fonts'),
        ('src/default/settings.json', 'src/default'),
        ('src/default/timesheet.csv', 'src/default'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Timer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Timer',
)
app = BUNDLE(
    coll,
    name='Timer.app',
    icon='resources/icon.icns',
    bundle_identifier=None,
)

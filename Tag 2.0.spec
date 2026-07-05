# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/main.py'],
    pathex=[],
    binaries=[('/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/build_assets/ffmpeg', '.'), ('/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/build_assets/ffprobe', '.')],
    datas=[('/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/assets', 'assets')],
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
    a.binaries,
    a.datas,
    [],
    name='Tag 2.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/build_assets/icon.icns'],
)
app = BUNDLE(
    exe,
    name='Tag 2.0.app',
    icon='/Users/diegogalindo/my_stuff/01_Projects/Sergio/Sergio_Game/tag_2_0/build_assets/icon.icns',
    bundle_identifier=None,
)

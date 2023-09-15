# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['dbus.mainloop.glib', 'dbus_fast._private.marshaller','dbus_fast._private.address','dbus_fast._private.constants','dbus_fast.__version__', 'dbus_fast._private', 'dbus_fast.aio', 'dbus_fast.auth', 'dbus_fast.constants', 'dbus_fast.errors', 'dbus_fast.glib', 'dbus_fast.introspection', 'dbus_fast.main', 'dbus_fast.message', 'dbus_fast.message_bus', 'dbus_fast.proxy_object', 'dbus_fast.service', 'dbus_fast.signature', 'dbus_fast.unpack', 'dbus_fast.validators'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

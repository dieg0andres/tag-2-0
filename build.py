# build.py

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

APP_NAME = "Tag 2.0"
ENTRY_POINT = PROJECT_ROOT / "main.py"

ASSETS_DIR = PROJECT_ROOT / "assets"

BUILD_ASSETS_DIR = PROJECT_ROOT / "build_assets"
ICON_FILE = BUILD_ASSETS_DIR / "icon.icns"
FFMPEG_FILE = BUILD_ASSETS_DIR / "ffmpeg"
FFPROBE_FILE = BUILD_ASSETS_DIR / "ffprobe"

PYVIDPLAYER_IMPORT_CHECK = """
import importlib.util

original_find_spec = importlib.util.find_spec

def guarded_find_spec(name, *args, **kwargs):
    if name == "tkinter":
        return None
    return original_find_spec(name, *args, **kwargs)

importlib.util.find_spec = guarded_find_spec

from pyvidplayer2 import READER_FFMPEG, Video, set_ffmpeg_path, set_ffprobe_path

assert READER_FFMPEG is not None
assert Video is not None
assert set_ffmpeg_path is not None
assert set_ffprobe_path is not None
"""

BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"


def require_file(path: Path, description: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {description}: {path}")


def require_dir(path: Path, description: str) -> None:
    if not path.is_dir():
        raise FileNotFoundError(f"Missing {description}: {path}")


def require_import(import_statement: str, description: str) -> None:
    result = subprocess.run(
        [sys.executable, "-c", import_statement],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        raise RuntimeError(
            f"Missing or broken {description} in the active build interpreter: {sys.executable}\n{details}"
        )


def require_executable(path: Path, description: str) -> None:
    require_file(path, description)
    if not os.access(path, os.X_OK):
        raise PermissionError(f"{description} is not executable: {path}")


def describe_binary(path: Path) -> str:
    try:
        result = subprocess.run(
            ["file", str(path)],
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return f"Unable to inspect {path}: {exc}"
    return result.stdout.strip() or result.stderr.strip() or f"No architecture details for {path}"


def run_preflight_checks() -> None:
    require_file(ENTRY_POINT, "entry point")
    require_dir(ASSETS_DIR, "assets directory")
    require_file(ICON_FILE, "macOS icon file")
    require_executable(FFMPEG_FILE, "FFmpeg binary")
    require_executable(FFPROBE_FILE, "FFprobe binary")
    require_import("import PyInstaller", "PyInstaller package")
    require_import(PYVIDPLAYER_IMPORT_CHECK, "pyvidplayer2 pygame video package")

    print("Build preflight:")
    print(f"  Python: {sys.executable}")
    print(f"  Machine architecture: {platform.machine()}")
    print(f"  FFmpeg: {describe_binary(FFMPEG_FILE)}")
    print(f"  FFprobe: {describe_binary(FFPROBE_FILE)}")
    print()


def clean_previous_build() -> None:
    for path in [BUILD_DIR, DIST_DIR]:
        if path.exists():
            print(f"Removing {path}")
            shutil.rmtree(path)

    for spec_file in PROJECT_ROOT.glob("*.spec"):
        print(f"Removing {spec_file}")
        spec_file.unlink()


def build_app() -> None:
    run_preflight_checks()

    command = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--name",
        APP_NAME,

        "--windowed",
        "--onefile",

        "--icon",
        str(ICON_FILE),

        "--add-data",
        f"{ASSETS_DIR}:assets",

        "--add-binary",
        f"{FFMPEG_FILE}:.",

        "--add-binary",
        f"{FFPROBE_FILE}:.",

        str(ENTRY_POINT),
    ]

    print("Running PyInstaller command:")
    print(" ".join(command))
    print()

    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def main() -> None:
    clean_previous_build()
    build_app()

    app_path = DIST_DIR / f"{APP_NAME}.app"

    print()
    print("Build complete.")
    print(f"App created at: {app_path}")
    print()
    print("Run it with:")
    print(f'open "{app_path}"')


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Build script for creating a Linux AppImage distribution of AI Assessor.

Run this script on a Linux machine to create a distributable AppImage.

IMPORTANT: This script should be run in a virtual environment:
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. pip install pyinstaller
5. python build_linux.py
"""

import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


def build_linux_appimage():
    """
    Build a Linux AppImage with PyInstaller and prepare the distribution.
    """
    print("Beginning build process for AI Assessor Linux AppImage...")

    # Check if we're in a virtual environment
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("WARNING: Not running in a virtual environment!")
        print("Please create and activate a virtual environment:")
        print("1. python -m venv venv")
        print("2. source venv/bin/activate")
        print("3. pip install -r requirements.txt")
        print("4. pip install pyinstaller")
        print("5. python build_linux.py")
        return False

    try:
        # Clean previous builds
        print("Cleaning previous builds...")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("AI_Assessor.AppDir"):
            shutil.rmtree("AI_Assessor.AppDir")

        # Build with PyInstaller
        print("Building executable with PyInstaller...")
        subprocess.run(
            [
                "pyinstaller",
                "--onedir",
                "--windowed",
                "--name",
                "AI_Assessor",
                "--add-data",
                "prompts:prompts",
                "--add-data",
                "support:support",
                "--add-data",
                "submissions:submissions",
                "--hidden-import",
                "tkinter",
                "--hidden-import",
                "tkinter.ttk",
                "--hidden-import",
                "tkinter.messagebox",
                "--hidden-import",
                "tkinter.filedialog",
                "--hidden-import",
                "PIL._tkinter_finder",
                "ai_assessor_main.py",
            ],
            check=True,
        )

        print("PyInstaller build completed successfully.")

        # Download AppImage tools
        appimage_tool = "appimagetool-x86_64.AppImage"
        if not os.path.exists(appimage_tool):
            print("Downloading AppImage tools...")
            urllib.request.urlretrieve(
                "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage",
                appimage_tool,
            )
            os.chmod(appimage_tool, 0o755)

        # Create AppImage directory structure
        print("Creating AppImage directory structure...")
        appdir = Path("AI_Assessor.AppDir")
        appdir.mkdir(exist_ok=True)
        (appdir / "usr" / "bin").mkdir(parents=True, exist_ok=True)
        (appdir / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(
            parents=True, exist_ok=True
        )

        # Copy the built application
        print("Copying application files...")
        shutil.copytree("dist/AI_Assessor", appdir / "usr" / "bin", dirs_exist_ok=True)

        # Create desktop file
        desktop_content = """[Desktop Entry]
Name=AI Assessor
Exec=AI_Assessor
Icon=ai-assessor
Type=Application
Categories=Education;Office;
Comment=AI-powered tool for grading student submissions
"""
        with open(
            appdir / "usr" / "share" / "applications" / "ai-assessor.desktop", "w"
        ) as f:
            f.write(desktop_content)

        # Create SVG icon
        icon_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#2563eb" rx="32"/>
  <text x="128" y="140" font-family="sans-serif" font-size="80" fill="white" text-anchor="middle" font-weight="bold">AI</text>
  <text x="128" y="200" font-family="sans-serif" font-size="24" fill="#93c5fd" text-anchor="middle">Assessor</text>
</svg>"""
        with open(
            appdir
            / "usr"
            / "share"
            / "icons"
            / "hicolor"
            / "256x256"
            / "apps"
            / "ai-assessor.svg",
            "w",
        ) as f:
            f.write(icon_content)

        # Create AppRun script
        apprun_content = """#!/bin/bash
cd "$(dirname "$0")/usr/bin"
exec "./AI_Assessor" "$@"
"""
        with open(appdir / "AppRun", "w") as f:
            f.write(apprun_content)
        os.chmod(appdir / "AppRun", 0o755)

        # Copy files to root
        shutil.copy2(
            appdir / "usr" / "share" / "applications" / "ai-assessor.desktop",
            appdir / "ai-assessor.desktop",
        )
        shutil.copy2(
            appdir
            / "usr"
            / "share"
            / "icons"
            / "hicolor"
            / "256x256"
            / "apps"
            / "ai-assessor.svg",
            appdir / "ai-assessor.svg",
        )

        # Build AppImage
        print("Building AppImage...")
        subprocess.run(
            [f"./{appimage_tool}", str(appdir), "AI_Assessor-x86_64.AppImage"],
            check=True,
        )

        print("\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("AppImage created: AI_Assessor-x86_64.AppImage")

        if os.path.exists("AI_Assessor-x86_64.AppImage"):
            size_mb = os.path.getsize("AI_Assessor-x86_64.AppImage") / (1024 * 1024)
            print(f"AppImage size: {size_mb:.1f} MB")

        print("\nTo run the application:")
        print("./AI_Assessor-x86_64.AppImage")
        print("\nTo make it executable from anywhere:")
        print("chmod +x AI_Assessor-x86_64.AppImage")
        print("mv AI_Assessor-x86_64.AppImage /usr/local/bin/ai-assessor")

        return True

    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print("Check the output above for details.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = build_linux_appimage()
    sys.exit(0 if success else 1)

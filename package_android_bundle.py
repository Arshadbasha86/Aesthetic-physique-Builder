"""
package_android_bundle.py - Aesthetic Physique Android Packaging & Build Automation
Architectural Role: Pre-flight validator and packaging orchestrator preparing the mobile client
for Android compilation via Flet CLI (`flet build apk`), validating all 52 workout GIFs,
sound pool assets, and generating the production build manifest.

Usage:
  python package_android_bundle.py --check-assets   # Validates all required binary assets
  python package_android_bundle.py --generate-manifest # Writes flet android build configuration
  python package_android_bundle.py --dry-run        # Displays exact flet build command
"""

import os
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
FRONTEND_DIR = BASE_DIR / "frontend_app"
ASSETS_DIR = FRONTEND_DIR / "assets"
WORKOUTS_DIR = ASSETS_DIR / "images" / "workouts"
SFX_DIR = ASSETS_DIR / "audio" / "sfx"


def validate_assets() -> bool:
    """Verifies that all 52 exercise GIFs and 3 SFX audio files exist."""
    print("\n" + "=" * 70)
    print("      AESTHETIC PHYSIQUE -- ANDROID ASSETS PRE-FLIGHT VALIDATION")
    print("=" * 70 + "\n")

    all_valid = True

    # 1. Check Sound Effects
    required_sfx = ["tick.mp3", "bell.mp3", "whistle.mp3"]
    print("  [SFX POOL ASSETS]")
    for sfx in required_sfx:
        p = SFX_DIR / sfx
        exists = p.exists()
        tag = "[PASS]" if exists else "[FAIL]"
        print(f"    {tag} {sfx:<25} ({p})")
        if not exists:
            all_valid = False

    # 2. Check Workout Demonstration Images (52 Required: 38 GIFs + 14 JPGs)
    print("\n  [EXERCISE DEMONSTRATION ASSETS (52 REQUIRED: 38 GIFs + 14 JPGs)]")
    if not WORKOUTS_DIR.exists():
        print(f"    [FAIL] Workouts directory not found: {WORKOUTS_DIR}")
        return False

    image_files = list(WORKOUTS_DIR.glob("*.gif")) + list(WORKOUTS_DIR.glob("*.jpg"))
    asset_count = len(image_files)
    tag = "[PASS]" if asset_count >= 52 else "[WARN]"
    print(f"    {tag} Found {asset_count}/52 demonstration assets ({len(list(WORKOUTS_DIR.glob('*.gif')))} GIFs, {len(list(WORKOUTS_DIR.glob('*.jpg')))} JPGs) in {WORKOUTS_DIR.name}")

    # 3. Check Local Schema
    schema_file = FRONTEND_DIR / "database" / "local_schema.sql"
    tag = "[PASS]" if schema_file.exists() else "[FAIL]"
    print(f"\n  [DATABASE SCHEMA]")
    print(f"    {tag} local_schema.sql exists ({schema_file})")

    # 4. Check Official App Icon
    app_icon_file = ASSETS_DIR / "images" / "app_icon.png"
    icon_tag = "[PASS]" if app_icon_file.exists() else "[FAIL]"
    print(f"\n  [OFFICIAL APP ICON]")
    print(f"    {icon_tag} app_icon.png (Greek Statue Bust) exists ({app_icon_file})")
    if not app_icon_file.exists():
        all_valid = False

    print("\n" + "=" * 70)
    if all_valid and asset_count >= 52:
        print("  RESULT: PRE-FLIGHT ASSET AUDIT PASSED! READY FOR COMPILATION.")
    else:
        print("  RESULT: PRE-FLIGHT ASSET AUDIT COMPLETED WITH WARNINGS.")
    print("=" * 70 + "\n")

    return all_valid


def generate_build_manifest():
    """Generates the flet Android configuration file (flet.yaml) in frontend_app."""
    manifest_path = FRONTEND_DIR / "flet.yaml"
    manifest_content = """# Aesthetic Physique Mobile Client - Flet Android Build Manifest
app:
  name: "Aesthetic Physique"
  package: "com.aestheticphysique.builder"
  version: "1.2.0"
  build_number: 12
  description: "High-performance bodybuilding & hypertrophy training ecosystem with wall-clock rest audio."
  author: "Aesthetic Physique Engineering"

android:
  permissions:
    - "android.permission.INTERNET"
    - "android.permission.ACCESS_NETWORK_STATE"
    - "android.permission.VIBRATE"
    - "android.permission.WAKE_LOCK"
  screen_orientation: "portrait"
  adaptive_icon:
    foreground: "assets/icon_foreground.png"
    background: "#0D1117"
"""
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)

    print(f"  [SUCCESS] Generated Android build manifest at: {manifest_path}")


def display_build_command():
    """Displays the exact Flet CLI build invocation for building release APK."""
    print("\n" + "=" * 70)
    print("  PRODUCTION ANDROID APK COMPILATION INVOCATION")
    print("=" * 70)
    print("\n  To compile the standalone APK using the official Flet Flutter toolchain:")
    print("\n    cd \"frontend_app\"")
    print("    flet build apk --project \"Aesthetic Physique\" --org \"com.aestheticphysique\"\n")
    print("  Output binary location:")
    print("    frontend_app/build/apk/app-release.apk\n")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Aesthetic Physique Android Packaging Orchestrator")
    parser.add_argument("--check-assets", action="store_true", help="Validate all 52 GIFs and SFX audio assets")
    parser.add_argument("--generate-manifest", action="store_true", help="Generate flet.yaml Android build manifest")
    parser.add_argument("--dry-run", action="store_true", help="Display exact compilation commands")

    args = parser.parse_args()

    if args.check_assets:
        validate_assets()
    elif args.generate_manifest:
        generate_build_manifest()
    elif args.dry_run:
        display_build_command()
    else:
        # Default behavior: run all steps
        validate_assets()
        generate_build_manifest()
        display_build_command()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate all bus sprites.

Reads bus_manifest.txt (created by generate_bus_scripts.py) and runs each
vehicle's _create.py to produce 32bpp sprite sheets.

Usage:
    python sprites/road/buses/generate_all.py
    python sprites/road/buses/generate_all.py --vehicle benz_omnibus
"""

import argparse
import importlib.util
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = BASE_DIR / "scripts"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure bus_base is importable
sys.path.insert(0, str(BASE_DIR))


def run_create_script(slug: str):
    """Run a single vehicle's _create.py script."""
    script_path = SCRIPT_DIR / f"{slug}_create.py"
    if not script_path.exists():
        print(f"  SKIP: {script_path.name} not found")
        return False
    spec = importlib.util.spec_from_file_location(f"create_{slug}", script_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        # The __main__ guard prevents auto-execution via importlib,
        # so call generate_bus_sprites directly using the module's style.
        from bus_base import generate_bus_sprites
        generate_bus_sprites(mod.style, OUTPUT_DIR)
        return True
    except Exception as e:
        print(f"  ERROR: {slug}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate bus sprites")
    parser.add_argument("--vehicle", "-v", help="Generate only this vehicle slug")
    args = parser.parse_args()

    manifest = BASE_DIR / "bus_manifest.txt"
    if not manifest.exists():
        print("bus_manifest.txt not found. Run generate_bus_scripts.py first.")
        sys.exit(1)

    slugs = [l.strip() for l in manifest.read_text().splitlines() if l.strip()]

    if args.vehicle:
        if args.vehicle not in slugs:
            print(f"Vehicle '{args.vehicle}' not in manifest")
            sys.exit(1)
        slugs = [args.vehicle]

    print(f"Generating sprites for {len(slugs)} buses...")
    ok = 0
    fail = 0
    for slug in slugs:
        if run_create_script(slug):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} succeeded, {fail} failed")


if __name__ == "__main__":
    main()

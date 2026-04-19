#!/usr/bin/env python3
"""Top-level sprite generation: regenerate all sprites or a single group.

Usage:
    python sprites/generate_all.py                  # everything
    python sprites/generate_all.py --group buses    # just buses
    python sprites/generate_all.py --group trucks   # just trucks
    python sprites/generate_all.py --list           # list available groups
"""

import argparse
import subprocess
import sys
from pathlib import Path

SPRITES_DIR = Path(__file__).resolve().parent

# Map group names to their generate_all.py script
GROUPS = {
    "buses":    SPRITES_DIR / "road" / "buses" / "generate_all.py",
    # Future groups (uncomment as they are implemented):
    # "trucks":   SPRITES_DIR / "road" / "trucks" / "generate_all.py",
    # "cars":     SPRITES_DIR / "road" / "cars" / "generate_all.py",
    # "steam":    SPRITES_DIR / "trains" / "steam" / "generate_all.py",
    # "diesel":   SPRITES_DIR / "trains" / "diesel" / "generate_all.py",
    # "electric": SPRITES_DIR / "trains" / "electric" / "generate_all.py",
    # "dmu":      SPRITES_DIR / "trains" / "dmu-railcars" / "generate_all.py",
    # "emu":      SPRITES_DIR / "trains" / "emu-highspeed" / "generate_all.py",
    # "metro":    SPRITES_DIR / "trains" / "metro" / "generate_all.py",
    # "passenger_ships": SPRITES_DIR / "ships" / "passenger" / "generate_all.py",
    # "cargo_ships":     SPRITES_DIR / "ships" / "cargo" / "generate_all.py",
    # "airplanes":  SPRITES_DIR / "aircraft" / "airliners" / "generate_all.py",
    # "helicopters": SPRITES_DIR / "aircraft" / "helicopters" / "generate_all.py",
    # "airships":    SPRITES_DIR / "aircraft" / "airships" / "generate_all.py",
}


def run_group(name: str, script: Path, extra_args: list[str] = None):
    """Run a group's generate_all.py script."""
    if not script.exists():
        print(f"  SKIP: {name} — {script} not found")
        return False
    cmd = [sys.executable, str(script)] + (extra_args or [])
    print(f"\n{'='*60}")
    print(f"  Generating: {name}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=str(script.parent))
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Generate vehicle sprites")
    parser.add_argument("--group", "-g", help="Generate only this group")
    parser.add_argument("--vehicle", "-v",
                        help="Generate a single vehicle (requires --group)")
    parser.add_argument("--list", action="store_true",
                        help="List available groups")
    args = parser.parse_args()

    if args.list:
        print("Available groups:")
        for name, path in GROUPS.items():
            status = "ready" if path.exists() else "not yet implemented"
            print(f"  {name:20s} [{status}]")
        return

    if args.group:
        if args.group not in GROUPS:
            print(f"Unknown group: {args.group}")
            print(f"Available: {', '.join(GROUPS)}")
            sys.exit(1)
        extra = ["--vehicle", args.vehicle] if args.vehicle else []
        ok = run_group(args.group, GROUPS[args.group], extra)
        sys.exit(0 if ok else 1)

    # Run all groups
    results = {}
    for name, script in GROUPS.items():
        results[name] = run_group(name, script)

    print(f"\n{'='*60}")
    print("Summary:")
    for name, ok in results.items():
        print(f"  {name:20s} {'OK' if ok else 'FAILED'}")


if __name__ == "__main__":
    main()

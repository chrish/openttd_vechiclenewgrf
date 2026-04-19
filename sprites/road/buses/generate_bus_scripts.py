#!/usr/bin/env python3
"""Parse buses.nml and generate per-vehicle _create.py sprite scripts.

Reads vehicle definitions from the NML, determines era-appropriate colors
and style parameters, then writes a small _create.py for each bus into
sprites/road/buses/.

Run from project root:
    python sprites/road/buses/generate_bus_scripts.py
"""

import re
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent.parent.parent
NML_PATH = PROJ_ROOT / "road" / "buses" / "buses.nml"
BASE_DIR = Path(__file__).resolve().parent  # sprites/road/buses/
SCRIPT_DIR = BASE_DIR / "scripts"
OUTPUT_DIR = BASE_DIR / "output"

# ── Era-appropriate color palettes ────────────────────────────────────
# Each entry: (primary, secondary, trim)
EARLY_COLORS = [
    ((130, 30, 30), (95, 20, 20), (235, 215, 175)),   # maroon/cream
    ((30, 70, 40), (20, 50, 28), (200, 190, 150)),     # dark green
    ((80, 45, 25), (55, 30, 15), (210, 195, 160)),     # brown
    ((30, 35, 80), (20, 22, 55), (200, 200, 220)),     # navy
    ((100, 28, 28), (70, 18, 18), (220, 200, 160)),    # dark red
    ((50, 60, 40), (35, 42, 28), (195, 185, 150)),     # olive
    ((70, 30, 60), (48, 20, 42), (210, 190, 200)),     # plum
    ((45, 55, 70), (30, 38, 50), (200, 210, 220)),     # slate blue
]

CLASSIC_COLORS = [
    ((165, 30, 30), (120, 20, 20), (225, 205, 155)),   # red
    ((30, 90, 60), (20, 65, 42), (200, 220, 190)),     # green
    ((40, 45, 100), (28, 30, 72), (190, 195, 225)),    # blue
    ((130, 100, 30), (95, 72, 20), (230, 220, 170)),   # olive/gold
    ((155, 40, 40), (110, 28, 28), (240, 225, 180)),   # crimson
    ((45, 80, 90), (30, 58, 65), (195, 215, 220)),     # teal
    ((90, 50, 30), (65, 35, 20), (220, 200, 165)),     # rust
    ((75, 35, 85), (52, 24, 60), (215, 200, 220)),     # purple
    ((50, 70, 50), (35, 50, 35), (200, 215, 195)),     # forest green
    ((140, 60, 30), (100, 42, 20), (235, 215, 175)),   # burnt orange
]

MODERN_COLORS = [
    ((180, 35, 35), (130, 25, 25), (240, 240, 240)),   # bright red
    ((35, 100, 160), (25, 72, 115), (230, 240, 250)),  # blue
    ((40, 130, 70), (28, 95, 50), (230, 245, 235)),    # green
    ((200, 140, 30), (145, 100, 20), (250, 245, 220)), # yellow/gold
    ((90, 90, 90), (60, 60, 60), (220, 220, 220)),     # grey
    ((220, 220, 220), (180, 180, 180), (60, 60, 60)),  # white/silver
    ((160, 50, 50), (115, 35, 35), (240, 235, 230)),   # muted red
    ((50, 80, 130), (35, 58, 95), (225, 235, 245)),    # steel blue
    ((35, 110, 100), (25, 80, 72), (225, 245, 240)),   # teal
    ((140, 80, 40), (100, 58, 28), (240, 230, 215)),   # khaki
]

CONTEMPORARY_COLORS = [
    ((30, 120, 190), (20, 88, 140), (240, 245, 255)),  # electric blue
    ((50, 170, 80), (35, 125, 58), (235, 250, 240)),   # eco green
    ((200, 60, 60), (145, 42, 42), (250, 245, 240)),   # red
    ((240, 240, 245), (195, 195, 200), (50, 50, 55)),  # white
    ((60, 60, 65), (42, 42, 46), (230, 230, 235)),     # charcoal
    ((180, 130, 40), (130, 95, 28), (250, 248, 235)),  # gold
    ((100, 50, 150), (72, 35, 110), (235, 225, 250)),  # purple
    ((30, 90, 120), (20, 65, 88), (230, 240, 248)),    # ocean blue
]

FUTURISTIC_COLORS = [
    ((220, 225, 235), (170, 175, 185), (40, 180, 220)),  # silver/cyan
    ((40, 180, 220), (28, 130, 160), (240, 245, 252)),   # cyan
    ((180, 60, 200), (130, 42, 145), (240, 230, 250)),   # magenta
    ((50, 200, 120), (35, 145, 88), (235, 252, 242)),    # neo green
    ((255, 180, 40), (185, 130, 28), (252, 248, 235)),   # amber
    ((60, 70, 90), (42, 50, 65), (200, 210, 230)),       # dark steel
    ((200, 200, 210), (150, 150, 158), (60, 200, 160)),  # pearl/green
    ((80, 50, 160), (58, 35, 115), (210, 200, 240)),     # deep purple
]


def _colors_for_year(year: int, index: int):
    """Pick colors based on year and an index for variety."""
    if year < 1925:
        pal = EARLY_COLORS
    elif year < 1960:
        pal = CLASSIC_COLORS
    elif year < 2000:
        pal = MODERN_COLORS
    elif year < 2035:
        pal = CONTEMPORARY_COLORS
    else:
        pal = FUTURISTIC_COLORS
    entry = pal[index % len(pal)]
    return entry  # (primary, secondary, trim)


def _body_length_from_capacity(cap: int) -> float:
    """Estimate body length ratio from cargo capacity."""
    if cap <= 12:   return 0.55
    if cap <= 20:   return 0.65
    if cap <= 35:   return 0.75
    if cap <= 55:   return 0.80
    if cap <= 80:   return 0.85
    if cap <= 120:  return 0.90
    return 0.95


def _slug_from_item(item_name: str) -> str:
    """Convert NML item name to a file slug: item_benz_omnibus -> benz_omnibus"""
    return item_name.replace("item_", "", 1)


def parse_buses_nml(nml_path: Path):
    """Parse buses.nml and yield vehicle dicts."""
    text = nml_path.read_text(encoding="utf-8")

    # Split into blocks by the separator comments
    pattern = re.compile(
        r'/\*\s*─+\s*\*/\s*\n'
        r'/\*\s+#(\d+)\s+(.+?)\s+\((\d{4})\)\s+\*/\s*\n'
        r'/\*\s+(.+?)\s+\*/\s*\n'
        r'/\*\s*─+\s*\*/\s*\n\s*'
        r'item\(FEAT_ROADVEHS,\s*(item_\w+),\s*(\d+)\)\s*\{(.*?)\n\}',
        re.DOTALL
    )

    for m in pattern.finditer(text):
        num = int(m.group(1))
        name = m.group(2).strip()
        year = int(m.group(3))
        description = m.group(4).strip()
        item_name = m.group(5)
        item_id = int(m.group(6))
        props_block = m.group(7)

        # Extract key properties
        cap_m = re.search(r'cargo_capacity:\s*(\d+)', props_block)
        spd_m = re.search(r'speed:\s*(\d+)', props_block)
        capacity = int(cap_m.group(1)) if cap_m else 20
        speed = int(spd_m.group(1)) if spd_m else 30

        double_deck = "double" in description.lower() or "double" in name.lower()

        yield {
            "num": num,
            "name": name,
            "year": year,
            "description": description,
            "item_name": item_name,
            "item_id": item_id,
            "capacity": capacity,
            "speed": speed,
            "double_deck": double_deck,
        }


def generate_create_script(vehicle: dict, index: int, out_dir: Path):
    """Write a _create.py script for one bus."""
    slug = _slug_from_item(vehicle["item_name"])
    name = vehicle["name"].replace('\u201c', '"').replace('\u201d', '"')
    year = vehicle["year"]
    desc = vehicle["description"].replace('\u201c', '"').replace('\u201d', '"')
    dd = vehicle["double_deck"]
    cap = vehicle["capacity"]
    body_len = _body_length_from_capacity(cap)

    primary, secondary, trim = _colors_for_year(year, index)

    name_repr = repr(name)

    script = f'''#!/usr/bin/env python3
"""Generate sprites for {name} ({year}).

{desc}
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="{slug}",
    name={name_repr},
    year={year},
    double_deck={dd},
    body_length={body_len},
    primary={primary + (255,)},
    secondary={secondary + (255,)},
    trim={trim + (255,)},
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")
'''
    out_path = out_dir / f"{slug}_create.py"
    out_path.write_text(script, encoding="utf-8")
    return slug


def main():
    print(f"Reading: {NML_PATH}")
    vehicles = list(parse_buses_nml(NML_PATH))
    print(f"Found {len(vehicles)} bus definitions")

    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    created = []
    for i, v in enumerate(vehicles):
        slug = generate_create_script(v, i, SCRIPT_DIR)
        created.append(slug)

    print(f"\nGenerated {len(created)} _create.py scripts in {SCRIPT_DIR}/")

    # Write a manifest for the generate_all script
    manifest_path = BASE_DIR / "bus_manifest.txt"
    manifest_path.write_text("\n".join(created) + "\n", encoding="utf-8")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()

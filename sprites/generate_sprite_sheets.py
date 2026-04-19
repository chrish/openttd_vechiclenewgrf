#!/usr/bin/env python3
"""
Generate blank 32bpp sprite sheet templates for OpenTTD vehicles.

Creates transparent RGBA PNG files with:
- Grid lines showing sprite boundaries
- Labels for each directional view (N, NE, E, SE, S, SW, W, NW)
- Correct sizes for 1x and 4x zoom levels
- Separate sheets for each vehicle type

Usage:
    python generate_sprite_sheets.py [--type TYPE] [--rows N]

    --type   Vehicle type: road, train, aircraft, aircraft_small, ship, all (default: all)
    --rows   Number of vehicle rows per sheet (default: 4)
"""

import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow is required. Install with: pip install Pillow")
    raise SystemExit(1)


# Sprite definitions: (x_offset, width, height, label)
# x_offset is the starting X position in the 1x sheet
VEHICLE_TYPES = {
    "road": {
        "row_height": 20,
        "views": [
            (0,    8, 18, "N"),
            (16,  20, 19, "NE"),
            (48,  28, 15, "E"),
            (96,  20, 19, "SE"),
            (128,  8, 18, "S"),
            (144, 20, 19, "SW"),
            (176, 28, 15, "W"),
            (224, 20, 19, "NW"),
        ],
    },
    "train": {  # Same as road
        "row_height": 20,
        "views": [
            (0,    8, 18, "N"),
            (16,  20, 19, "NE"),
            (48,  28, 15, "E"),
            (96,  20, 19, "SE"),
            (128,  8, 18, "S"),
            (144, 20, 19, "SW"),
            (176, 28, 15, "W"),
            (224, 20, 19, "NW"),
        ],
    },
    "aircraft": {
        "row_height": 40,
        "views": [
            (0,   24, 36, "N"),
            (32,  36, 28, "NE"),
            (80,  48, 20, "E"),
            (140, 36, 28, "SE"),
            (188, 24, 36, "S"),
            (220, 36, 28, "SW"),
            (268, 48, 20, "W"),
            (328, 36, 28, "NW"),
        ],
    },
    "aircraft_small": {
        "row_height": 28,
        "views": [
            (0,   16, 24, "N"),
            (24,  24, 20, "NE"),
            (56,  32, 14, "E"),
            (100, 24, 20, "SE"),
            (132, 16, 24, "S"),
            (156, 24, 20, "SW"),
            (188, 32, 14, "W"),
            (228, 24, 20, "NW"),
        ],
    },
    "ship": {
        "row_height": 36,
        "views": [
            (0,   16, 32, "N"),
            (24,  32, 24, "NE"),
            (68,  48, 16, "E"),
            (128, 32, 24, "SE"),
            (168, 16, 32, "S"),
            (192, 32, 24, "SW"),
            (236, 48, 16, "W"),
            (296, 32, 24, "NW"),
        ],
    },
}

# Map vehicle types to output subdirectories
TYPE_SUBDIRS = {
    "road": "road",
    "train": "trains",
    "aircraft": "aircraft",
    "aircraft_small": "aircraft",
    "ship": "ships",
}

# Colors
GRID_COLOR = (100, 100, 100, 128)       # Semi-transparent grey grid
SPRITE_BORDER = (80, 180, 255, 180)     # Blue sprite boundaries
LABEL_COLOR = (200, 200, 200, 200)      # Light grey labels
BG_COLOR = (0, 0, 0, 0)                 # Fully transparent background


def generate_sheet(vehicle_type: str, num_rows: int, zoom: int, output_dir: Path):
    """Generate a sprite sheet template for a vehicle type at a given zoom level."""
    spec = VEHICLE_TYPES[vehicle_type]
    row_h = spec["row_height"] * zoom

    # Calculate sheet dimensions
    max_x = max(x + w for x, w, h, _ in spec["views"])
    sheet_w = max_x * zoom + 8 * zoom  # padding on right
    sheet_h = row_h * num_rows

    img = Image.new("RGBA", (sheet_w, sheet_h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to use a basic font; fall back to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", max(8, 6 * zoom))
    except (OSError, IOError):
        font = ImageFont.load_default()

    small_font = font
    try:
        small_font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", max(6, 4 * zoom))
    except (OSError, IOError):
        pass

    for row in range(num_rows):
        y_base = row * row_h

        # Row separator line
        draw.line([(0, y_base), (sheet_w - 1, y_base)], fill=GRID_COLOR, width=1)

        for x_1x, w_1x, h_1x, label in spec["views"]:
            x = x_1x * zoom
            w = w_1x * zoom
            h = h_1x * zoom

            # Draw sprite boundary rectangle
            draw.rectangle(
                [x, y_base, x + w - 1, y_base + h - 1],
                outline=SPRITE_BORDER,
                width=1,
            )

            # Draw crosshair at center
            cx = x + w // 2
            cy = y_base + h // 2
            cross_size = max(2, 3 * zoom)
            draw.line([(cx - cross_size, cy), (cx + cross_size, cy)], fill=GRID_COLOR, width=1)
            draw.line([(cx, cy - cross_size), (cx, cy + cross_size)], fill=GRID_COLOR, width=1)

            # Label
            draw.text((x + 2, y_base + 1), label, fill=LABEL_COLOR, font=small_font)

            # Size label at bottom of sprite
            size_text = f"{w_1x}x{h_1x}"
            draw.text((x + 2, y_base + h - 6 * zoom), size_text, fill=GRID_COLOR, font=small_font)

        # Row number label on the right
        draw.text(
            (sheet_w - 20 * zoom, y_base + 2),
            f"Row {row}",
            fill=LABEL_COLOR,
            font=small_font,
        )

    # Bottom border
    draw.line([(0, sheet_h - 1), (sheet_w - 1, sheet_h - 1)], fill=GRID_COLOR, width=1)

    # Build filename
    zoom_label = f"{zoom}x"
    filename = f"{vehicle_type}_{zoom_label}_32bpp.png"
    filepath = output_dir / filename
    img.save(filepath, "PNG")
    print(f"  Created: {filepath} ({sheet_w}x{sheet_h})")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate 32bpp sprite sheet templates")
    parser.add_argument("--type", default="all", choices=list(VEHICLE_TYPES.keys()) + ["all"],
                        help="Vehicle type to generate (default: all)")
    parser.add_argument("--rows", type=int, default=4,
                        help="Number of vehicle rows per sheet (default: 4)")
    args = parser.parse_args()

    base_dir = Path(__file__).parent

    types_to_generate = list(VEHICLE_TYPES.keys()) if args.type == "all" else [args.type]

    for vtype in types_to_generate:
        subdir = TYPE_SUBDIRS[vtype]
        output_dir = base_dir / subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n{vtype.upper()} sprites -> {subdir}/")
        # Generate 1x (normal zoom) and 4x (extra zoom) sheets
        generate_sheet(vtype, args.rows, zoom=1, output_dir=output_dir)
        generate_sheet(vtype, args.rows, zoom=4, output_dir=output_dir)

    print(f"\nDone! Template sprite sheets saved to: {output_dir}/")
    print("These are transparent PNGs with guide overlays.")
    print("Draw your vehicle sprites within the blue rectangles.")
    print("Remove the guide overlays before compiling your GRF.")


if __name__ == "__main__":
    main()

---
description: "Use when creating, editing, or generating 32bpp sprites, sprite sheets, 8bpp palette fallbacks, or wiring graphics into NML vehicle definitions. Covers the full workflow from pixel art through GRF compilation."
applyTo: "sprites/**"
---

# 32bpp Vehicle Graphics Workflow

## Architecture Overview

```
sprites/
├── templates.nml              # NML template definitions (include in your main NML)
├── generate_sprite_sheets.py  # Generates blank template PNGs with guides
├── README.md                  # Quick reference for sizes and offsets
├── tools/
│   ├── convert_8bpp.py        # Converts 32bpp RGBA → 8bpp TTD palette PNGs
│   └── ttd_dos_palette.bin    # Canonical 768-byte DOS palette from nmlc
├── aircraft/                  # Aircraft + helicopter sprite sheets
├── road/                      # Road vehicle sprite sheets
├── ships/                     # Ship sprite sheets
└── trains/                    # Train sprite sheets
```

## Color Depth Requirements

- **32bpp**: Full RGBA PNG. This is where you draw. Transparency via alpha channel.
- **8bpp**: Indexed PNG using the exact TTD DOS palette. Required as the base `spriteset` fallback. nmlc validates the palette byte-for-byte.

### Generating 8bpp Fallbacks

Always use `sprites/tools/convert_8bpp.py` which loads the canonical palette from `ttd_dos_palette.bin` (extracted from `nml.palette.palette_data[0]`). Never hand-code the palette — it must match exactly or nmlc rejects it.

```sh
source .venv/bin/activate && python sprites/tools/convert_8bpp.py
```

**Key palette fact**: Index 0 = `(0, 0, 255)` (blue), NOT `(0, 0, 0)`. This is the transparent color.

## Sprite Templates

All templates are in `sprites/templates.nml`. They use a zoom-scaling core template:

```nml
template tmpl_zoom(x, y, w, h, ox, oy, zoom) {
    [x * zoom, y * zoom, w * zoom, h * zoom, ox * zoom, oy * zoom - (zoom / 2)]
}
```

### Available Templates

| Template | Vehicle Type | Row Height (1x) |
|----------|-------------|-----------------|
| `tmpl_road_train(row, zoom)` | Road vehicles & trains | 20px |
| `tmpl_aircraft(row, zoom)` | Medium/large aircraft | 40px |
| `tmpl_aircraft_small(row, zoom)` | Small aircraft & helicopters | 28px |
| `tmpl_ship(row, zoom)` | Ships | 36px |
| `tmpl_purchase(x, y, zoom)` | Purchase menu (single sprite) | — |

Each template produces 8 directional views: N, NE, E, SE, S, SW, W, NW.

### Sprite Sizes at 1x Zoom

**Road Vehicles / Trains:**

| View | W×H | Offset |
|------|-----|--------|
| N | 8×18 | (-3, -10) |
| NE | 20×19 | (-14, -5) |
| E | 28×15 | (-14, -8) |
| SE | 20×19 | (-6, -7) |
| S | 8×18 | (-3, -10) |
| SW | 20×19 | (-14, -9) |
| W | 28×15 | (-14, -8) |
| NW | 20×19 | (-6, -7) |

**Aircraft (large):**

| View | W×H | Offset |
|------|-----|--------|
| N | 24×36 | (-12, -28) |
| NE | 36×28 | (-28, -18) |
| E | 48×20 | (-24, -12) |
| SE | 36×28 | (-8, -18) |
| S | 24×36 | (-12, -28) |
| SW | 36×28 | (-28, -18) |
| W | 48×20 | (-24, -12) |
| NW | 36×28 | (-8, -18) |

**Ships:**

| View | W×H | Offset |
|------|-----|--------|
| N | 16×32 | (-8, -24) |
| NE | 32×24 | (-24, -14) |
| E | 48×16 | (-24, -10) |
| SE | 32×24 | (-8, -14) |
| S | 16×32 | (-8, -24) |
| SW | 32×24 | (-24, -14) |
| W | 48×16 | (-24, -10) |
| NW | 32×24 | (-8, -14) |

## Zoom Levels

| NML Constant | Multiplier | Usage |
|---|---|---|
| `ZOOM_LEVEL_NORMAL` | 1x | Base resolution |
| `ZOOM_LEVEL_IN_2X` | 2x | Extra zoom |
| `ZOOM_LEVEL_IN_4X` | 4x | Extra zoom (recommended for 32bpp detail) |

For Nx zoom, multiply all sprite coordinates, sizes, AND X offsets by N. Y offset scales as: `oy_Nx = oy_1x * N - (N / 2)`. This is handled automatically by `tmpl_zoom`.

## Creating Sprites for a Vehicle

### Step 1: Draw the 32bpp art

Work at **4x zoom** for detail. Create 8 directional views laid out in a row matching the template positions. Save as RGBA PNG.

For programmatic sprite generation (like `milnes_daimler_create.py`), use the view coordinates from `VIEWS_4X`:

```python
VIEWS_4X = [
    ("N",   0,   0, 32, 72),   # (name, x, y, width, height)
    ("NE", 64,   0, 80, 76),
    ("E", 192,   0, 112, 60),
    ("SE", 384,  0, 80, 76),
    ("S",  512,  0, 32, 72),
    ("SW", 576,  0, 80, 76),
    ("W",  704,  0, 112, 60),
    ("NW", 896,  0, 80, 76),
]
```

Use `Image.FLIP_LEFT_RIGHT` for mirrored views (W from E, SE from NE, NW from SW, S from N+adjustments).

### Step 2: Generate 1x version

Scale the 4x PNG down by 4× using `Image.LANCZOS`:

```python
sheet_1x = sheet_4x.resize((w // 4, h // 4), Image.LANCZOS)
```

### Step 3: Generate 8bpp fallback

```sh
python sprites/tools/convert_8bpp.py
```

Or adapt it for your specific files. The converter reads `ttd_dos_palette.bin` and maps each non-transparent pixel to the nearest palette color.

### Step 4: Wire into NML

```nml
// Include templates
#include "sprites/templates.nml"

// 8bpp base (required by nmlc)
spriteset(my_vehicle_set, "sprites/road/my_vehicle_1x_8bpp.png") {
    tmpl_road_train(0, 1)
}

// 32bpp at normal zoom
alternative_sprites(my_vehicle_set, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP,
                    "sprites/road/my_vehicle_1x.png") {
    tmpl_road_train(0, 1)
}

// 32bpp at 4x extra zoom
alternative_sprites(my_vehicle_set, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP,
                    "sprites/road/my_vehicle_4x.png") {
    tmpl_road_train(0, 4)
}
```

### Step 5: Attach to the vehicle item

```nml
item(FEAT_ROADVEHS, item_my_vehicle, 1234) {
    property { /* ... */ }
    graphics {
        default: my_vehicle_set;
    }
}
```

### Step 6: Compile

```sh
source .venv/bin/activate
nmlc --lang-dir=lang_test --grf=output.grf source.nml
```

## File Naming Convention

For vehicle `foo_bar`:
- `sprites/<type>/foo_bar_4x.png` — 32bpp 4x zoom (detailed art)
- `sprites/<type>/foo_bar_1x.png` — 32bpp 1x zoom (scaled down)
- `sprites/<type>/foo_bar_1x_8bpp.png` — 8bpp palette fallback
- `sprites/<type>/foo_bar_4x_8bpp.png` — 8bpp palette fallback at 4x (optional)
- `sprites/<type>/foo_bar_create.py` — Generator script (if programmatic)

## Common Pitfalls

1. **Palette mismatch**: nmlc rejects 8bpp PNGs whose palette doesn't match byte-for-byte. Always use the extracted `ttd_dos_palette.bin`, never a hand-made palette.
2. **Index 0 is blue (0,0,255)**, not black. This is the transparent color in TTD DOS palette.
3. **Animation palette warnings**: If 8bpp pixels land on animation-range indices (e.g., water cycle colors), nmlc warns about ANIM flag. These are harmless for vehicle sprites.
4. **Base spriteset must be 8bpp**: The `spriteset()` block requires an 8bpp palette PNG. Use `alternative_sprites()` for 32bpp.
5. **Y offset scaling**: At Nx zoom, `offset_y = offset_y_1x * N - (N / 2)`. The `tmpl_zoom` template handles this.
6. **Sprite sheet layout must match template**: X positions and row heights must exactly match what the template expects. Use `generate_sprite_sheets.py` to create guides.

## Reference Example

See the complete Milnes-Daimler Double-Decker implementation:
- Generator: `sprites/road/milnes_daimler_create.py`
- 32bpp sprites: `sprites/road/milnes_daimler_4x.png`, `sprites/road/milnes_daimler_1x.png`
- 8bpp fallback: `sprites/road/milnes_daimler_1x_8bpp.png`
- Test NML: `test_milnes_daimler.nml` (standalone GRF with sprites wired up)

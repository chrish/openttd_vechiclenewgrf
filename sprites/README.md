# 32bpp Sprite Templates

Sprite sheet templates for the Darwin Vehicle Set. All sprites are 32bpp RGBA PNGs.

## Files

| File | Purpose |
|---|---|
| `templates.nml` | NML template definitions — include in your main NML |
| `generate_sprite_sheets.py` | Script to regenerate blank template PNGs |
| `*_1x_32bpp.png` | Normal zoom (1x) template sheets |
| `*_4x_32bpp.png` | Extra zoom (4x) template sheets |

## Sprite Sizes (1x Zoom)

### Road Vehicles / Trains

| View | Width | Height | Offset X | Offset Y |
|------|-------|--------|----------|----------|
| N    | 8     | 18     | -3       | -10      |
| NE   | 20    | 19     | -14      | -5       |
| E    | 28    | 15     | -14      | -8       |
| SE   | 20    | 19     | -6       | -7       |
| S    | 8     | 18     | -3       | -10      |
| SW   | 20    | 19     | -14      | -9       |
| W    | 28    | 15     | -14      | -8       |
| NW   | 20    | 19     | -6       | -7       |

### Aircraft (Medium/Large)

| View | Width | Height | Offset X | Offset Y |
|------|-------|--------|----------|----------|
| N    | 24    | 36     | -12      | -28      |
| NE   | 36    | 28     | -28      | -18      |
| E    | 48    | 20     | -24      | -12      |
| SE   | 36    | 28     | -8       | -18      |
| S    | 24    | 36     | -12      | -28      |
| SW   | 36    | 28     | -28      | -18      |
| W    | 48    | 20     | -24      | -12      |
| NW   | 36    | 28     | -8       | -18      |

### Aircraft (Small / Helicopters)

| View | Width | Height | Offset X | Offset Y |
|------|-------|--------|----------|----------|
| N    | 16    | 24     | -8       | -18      |
| NE   | 24    | 20     | -18      | -12      |
| E    | 32    | 14     | -16      | -8       |
| SE   | 24    | 20     | -6       | -12      |
| S    | 16    | 24     | -8       | -18      |
| SW   | 24    | 20     | -18      | -12      |
| W    | 32    | 14     | -16      | -8       |
| NW   | 24    | 20     | -6       | -12      |

### Ships

| View | Width | Height | Offset X | Offset Y |
|------|-------|--------|----------|----------|
| N    | 16    | 32     | -8       | -24      |
| NE   | 32    | 24     | -24      | -14      |
| E    | 48    | 16     | -24      | -10      |
| SE   | 32    | 24     | -8       | -14      |
| S    | 16    | 32     | -8       | -24      |
| SW   | 32    | 24     | -24      | -14      |
| W    | 48    | 16     | -24      | -10      |
| NW   | 32    | 24     | -8       | -14      |

## Zoom Levels

| Zoom | Multiplier | Description |
|------|-----------|-------------|
| `ZOOM_LEVEL_NORMAL` | 1x | Standard resolution |
| `ZOOM_LEVEL_IN_2X`  | 2x | Extra zoom level 1 |
| `ZOOM_LEVEL_IN_4X`  | 4x | Extra zoom level 2 (recommended for 32bpp) |

For 4x zoom, multiply all sizes and X/Y positions by 4. Offsets scale as:
- `offset_x_4x = offset_x_1x * 4`
- `offset_y_4x = offset_y_1x * 4 - 2`

## How to Use

### 1. Draw your sprites

Open the `_4x_32bpp.png` template for your vehicle type. Each row represents one vehicle. Draw each of the 8 directional views inside the blue bounding boxes.

### 2. Include templates in your NML

```nml
// In your main NML file or vehicle-specific NML
#include "sprites/templates.nml"
```

### 3. Define spritesets

```nml
// 32bpp spriteset at normal zoom
spriteset(my_vehicle_set, "sprites/road_1x_32bpp.png") {
    tmpl_road_train(0, 1)  // row 0, 1x zoom
}

// 32bpp at 4x extra zoom
alternative_sprites(my_vehicle_set, ZOOM_LEVEL_IN_4X, BIT_DEPTH_32BPP,
                    "sprites/road_4x_32bpp.png") {
    tmpl_road_train(0, 4)  // row 0, 4x zoom
}
```

### 4. Attach to vehicles

```nml
item(FEAT_ROADVEHS, my_bus, 100) {
    property { /* ... */ }
    graphics { default: my_vehicle_set; }
}
```

## Regenerating Templates

```sh
# All vehicle types, 4 rows each
python sprites/generate_sprite_sheets.py

# Specific type, custom row count
python sprites/generate_sprite_sheets.py --type aircraft --rows 8
```

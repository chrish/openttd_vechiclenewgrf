#!/usr/bin/env python3
"""Generate sprites for Aurora AU-2 LightSpeed (2078).

Hypercar (enclosed aerodynamic shell, magnetic road)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aurora_au_2_lightspeed",
    name='Aurora AU-2 LightSpeed',
    year=2078,
    double_deck=False,
    body_length=0.55,
    primary=(60, 70, 90, 255),
    secondary=(42, 50, 65, 255),
    trim=(200, 210, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

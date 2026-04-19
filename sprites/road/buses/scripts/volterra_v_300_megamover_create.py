#!/usr/bin/env python3
"""Generate sprites for Volterra V-300 MegaMover (2035).

Tri-articulated electric (ultra-capacity urban)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volterra_v_300_megamover",
    name='Volterra V-300 MegaMover',
    year=2035,
    double_deck=False,
    body_length=0.95,
    primary=(40, 180, 220, 255),
    secondary=(28, 130, 160, 255),
    trim=(240, 245, 252, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

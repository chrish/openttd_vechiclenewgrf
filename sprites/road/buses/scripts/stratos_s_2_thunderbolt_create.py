#!/usr/bin/env python3
"""Generate sprites for Stratos S-2 Thunderbolt (2070).

Hypercar (magnetic road assist, track-day legal)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="stratos_s_2_thunderbolt",
    name='Stratos S-2 Thunderbolt',
    year=2070,
    double_deck=False,
    body_length=0.55,
    primary=(220, 225, 235, 255),
    secondary=(170, 175, 185, 255),
    trim=(40, 180, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

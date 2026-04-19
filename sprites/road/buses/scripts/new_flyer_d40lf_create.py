#!/usr/bin/env python3
"""Generate sprites for New Flyer D40LF (1991).

Single-deck (first North American low-floor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="new_flyer_d40lf",
    name='New Flyer D40LF',
    year=1991,
    double_deck=False,
    body_length=0.85,
    primary=(220, 220, 220, 255),
    secondary=(180, 180, 180, 255),
    trim=(60, 60, 60, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

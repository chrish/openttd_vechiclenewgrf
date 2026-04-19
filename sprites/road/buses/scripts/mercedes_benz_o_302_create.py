#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 302 (1962).

Single-deck (touring coach, very successful)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_302",
    name='Mercedes-Benz O 302',
    year=1962,
    double_deck=False,
    body_length=0.8,
    primary=(90, 90, 90, 255),
    secondary=(60, 60, 60, 255),
    trim=(220, 220, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for MAN Lion's City 18 E (2021).

Articulated (German electric artic)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="man_lions_city_18_e",
    name="MAN Lion's City 18 E",
    year=2021,
    double_deck=False,
    body_length=0.9,
    primary=(30, 90, 120, 255),
    secondary=(20, 65, 88, 255),
    trim=(230, 240, 248, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

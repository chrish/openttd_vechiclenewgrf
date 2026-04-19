#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 305G (1975).

Articulated (German standard articulated bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_305g",
    name='Mercedes-Benz O 305G',
    year=1975,
    double_deck=False,
    body_length=0.9,
    primary=(35, 110, 100, 255),
    secondary=(25, 80, 72, 255),
    trim=(225, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

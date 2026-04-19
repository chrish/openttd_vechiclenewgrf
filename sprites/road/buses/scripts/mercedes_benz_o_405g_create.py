#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 405G (1990).

Articulated (German standard artic)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_405g",
    name='Mercedes-Benz O 405G',
    year=1990,
    double_deck=False,
    body_length=0.9,
    primary=(90, 90, 90, 255),
    secondary=(60, 60, 60, 255),
    trim=(220, 220, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

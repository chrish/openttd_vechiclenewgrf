#!/usr/bin/env python3
"""Generate sprites for Cascadia C-400 Superliner (2040).

Bi-articulated double-deck (mega-capacity BRT)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="cascadia_c_400_superliner",
    name='Cascadia C-400 Superliner',
    year=2040,
    double_deck=True,
    body_length=0.95,
    primary=(60, 70, 90, 255),
    secondary=(42, 50, 65, 255),
    trim=(200, 210, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

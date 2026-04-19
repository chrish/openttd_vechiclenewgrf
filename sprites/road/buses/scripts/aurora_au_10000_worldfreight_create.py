#!/usr/bin/env python3
"""Generate sprites for Aurora AU-10000 WorldFreight (2100).

Global mega-freight-train (automated transcontinental corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aurora_au_10000_worldfreight",
    name='Aurora AU-10000 WorldFreight',
    year=2100,
    double_deck=False,
    body_length=0.95,
    primary=(200, 200, 210, 255),
    secondary=(150, 150, 158, 255),
    trim=(60, 200, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

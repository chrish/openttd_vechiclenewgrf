#!/usr/bin/env python3
"""Generate sprites for Mack 6-BK (1930).

Single-deck (American city/intercity)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mack_6_bk",
    name='Mack 6-BK',
    year=1930,
    double_deck=False,
    body_length=0.75,
    primary=(130, 100, 30, 255),
    secondary=(95, 72, 20, 255),
    trim=(230, 220, 170, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

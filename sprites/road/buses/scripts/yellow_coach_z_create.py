#!/usr/bin/env python3
"""Generate sprites for Yellow Coach Z (1927).

Single-deck (early Greyhound-type coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="yellow_coach_z",
    name='Yellow Coach Z',
    year=1927,
    double_deck=False,
    body_length=0.75,
    primary=(50, 70, 50, 255),
    secondary=(35, 50, 35, 255),
    trim=(200, 215, 195, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

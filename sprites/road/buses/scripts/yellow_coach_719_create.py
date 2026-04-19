#!/usr/bin/env python3
"""Generate sprites for Yellow Coach 719 (1934).

Single-deck (American transit/Greyhound)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="yellow_coach_719",
    name='Yellow Coach 719',
    year=1934,
    double_deck=False,
    body_length=0.8,
    primary=(50, 70, 50, 255),
    secondary=(35, 50, 35, 255),
    trim=(200, 215, 195, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

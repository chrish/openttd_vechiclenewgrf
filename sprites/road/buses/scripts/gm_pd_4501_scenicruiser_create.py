#!/usr/bin/env python3
"""Generate sprites for GM PD-4501 Scenicruiser (1957).

Double-deck coach (Greyhound intercity)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="gm_pd_4501_scenicruiser",
    name='GM PD-4501 Scenicruiser',
    year=1957,
    double_deck=True,
    body_length=0.8,
    primary=(140, 60, 30, 255),
    secondary=(100, 42, 20, 255),
    trim=(235, 215, 175, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

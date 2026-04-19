#!/usr/bin/env python3
"""Generate sprites for Van Hool AG300 (1989).

Articulated (European city artic)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="van_hool_ag300",
    name='Van Hool AG300',
    year=1989,
    double_deck=False,
    body_length=0.9,
    primary=(200, 140, 30, 255),
    secondary=(145, 100, 20, 255),
    trim=(250, 245, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

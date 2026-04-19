#!/usr/bin/env python3
"""Generate sprites for Solaris Urbino 18 Electric (2014).

Articulated (Polish electric artic)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="solaris_urbino_18_electric",
    name='Solaris Urbino 18 Electric',
    year=2014,
    double_deck=False,
    body_length=0.9,
    primary=(30, 120, 190, 255),
    secondary=(20, 88, 140, 255),
    trim=(240, 245, 255, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

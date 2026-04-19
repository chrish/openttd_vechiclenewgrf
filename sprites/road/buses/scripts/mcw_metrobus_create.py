#!/usr/bin/env python3
"""Generate sprites for MCW Metrobus (1980).

Double-deck (standard British double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mcw_metrobus",
    name='MCW Metrobus',
    year=1980,
    double_deck=True,
    body_length=0.85,
    primary=(200, 140, 30, 255),
    secondary=(145, 100, 20, 255),
    trim=(250, 245, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for AEC Routemaster (1956).

Double-deck (iconic London bus, 1956–2005)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_routemaster",
    name='AEC Routemaster',
    year=1956,
    double_deck=True,
    body_length=0.85,
    primary=(50, 70, 50, 255),
    secondary=(35, 50, 35, 255),
    trim=(200, 215, 195, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

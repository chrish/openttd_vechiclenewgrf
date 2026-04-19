#!/usr/bin/env python3
"""Generate sprites for MAN MKN 26 (1959).

Single-deck (German city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="man_mkn_26",
    name='MAN MKN 26',
    year=1959,
    double_deck=False,
    body_length=0.8,
    primary=(30, 90, 60, 255),
    secondary=(20, 65, 42, 255),
    trim=(200, 220, 190, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

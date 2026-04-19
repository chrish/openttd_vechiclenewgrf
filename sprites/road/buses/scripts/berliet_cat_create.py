#!/usr/bin/env python3
"""Generate sprites for Berliet CAT (1906).

Single-deck (Paris omnibus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="berliet_cat",
    name='Berliet CAT',
    year=1906,
    double_deck=False,
    body_length=0.65,
    primary=(70, 30, 60, 255),
    secondary=(48, 20, 42, 255),
    trim=(210, 190, 200, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

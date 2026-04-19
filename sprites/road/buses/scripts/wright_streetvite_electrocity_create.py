#!/usr/bin/env python3
"""Generate sprites for Wright StreetVite / Electrocity (2009).

Single-deck (hybrid/electric British)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="wright_streetvite_electrocity",
    name='Wright StreetVite / Electrocity',
    year=2009,
    double_deck=False,
    body_length=0.8,
    primary=(200, 60, 60, 255),
    secondary=(145, 42, 42, 255),
    trim=(250, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

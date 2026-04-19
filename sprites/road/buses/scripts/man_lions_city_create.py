#!/usr/bin/env python3
"""Generate sprites for MAN Lion's City (A21) (1998).

Single-deck (European standard city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="man_lions_city",
    name="MAN Lion's City (A21)",
    year=1998,
    double_deck=False,
    body_length=0.8,
    primary=(200, 140, 30, 255),
    secondary=(145, 100, 20, 255),
    trim=(250, 245, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Fischer Omnibus (1899).

Single-deck (early Swiss motor bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="fischer_omnibus",
    name='Fischer Omnibus',
    year=1899,
    double_deck=False,
    body_length=0.55,
    primary=(80, 45, 25, 255),
    secondary=(55, 30, 15, 255),
    trim=(210, 195, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

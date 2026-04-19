#!/usr/bin/env python3
"""Generate sprites for Leyland Olympian (1984).

Double-deck (British/Hong Kong double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_olympian",
    name='Leyland Olympian',
    year=1984,
    double_deck=True,
    body_length=0.9,
    primary=(35, 110, 100, 255),
    secondary=(25, 80, 72, 255),
    trim=(225, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

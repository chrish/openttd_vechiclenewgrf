#!/usr/bin/env python3
"""Generate sprites for Volvo B7TL (1997).

Double-deck (British/Asian double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volvo_b7tl",
    name='Volvo B7TL',
    year=1997,
    double_deck=True,
    body_length=0.9,
    primary=(35, 100, 160, 255),
    secondary=(25, 72, 115, 255),
    trim=(230, 240, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

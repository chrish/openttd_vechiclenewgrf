#!/usr/bin/env python3
"""Generate sprites for Fageol Safety Coach (1922).

Single-deck (improved intercity coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="fageol_safety_coach",
    name='Fageol Safety Coach',
    year=1922,
    double_deck=False,
    body_length=0.75,
    primary=(70, 30, 60, 255),
    secondary=(48, 20, 42, 255),
    trim=(210, 190, 200, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

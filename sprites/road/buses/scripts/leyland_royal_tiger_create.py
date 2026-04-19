#!/usr/bin/env python3
"""Generate sprites for Leyland Royal Tiger (1953).

Single-deck (British express coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_royal_tiger",
    name='Leyland Royal Tiger',
    year=1953,
    double_deck=False,
    body_length=0.8,
    primary=(45, 80, 90, 255),
    secondary=(30, 58, 65, 255),
    trim=(195, 215, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Ikarus 556 (1966).

Single-deck (Hungarian city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ikarus_556",
    name='Ikarus 556',
    year=1966,
    double_deck=False,
    body_length=0.85,
    primary=(35, 110, 100, 255),
    secondary=(25, 80, 72, 255),
    trim=(225, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

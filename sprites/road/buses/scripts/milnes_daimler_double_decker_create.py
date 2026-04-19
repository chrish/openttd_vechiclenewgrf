#!/usr/bin/env python3
"""Generate sprites for Milnes-Daimler Double-Decker (1902).

Double-deck (early London motorbus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="milnes_daimler_double_decker",
    name='Milnes-Daimler Double-Decker',
    year=1902,
    double_deck=True,
    body_length=0.75,
    primary=(30, 35, 80, 255),
    secondary=(20, 22, 55, 255),
    trim=(200, 200, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

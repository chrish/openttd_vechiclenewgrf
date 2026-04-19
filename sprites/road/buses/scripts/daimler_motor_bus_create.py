#!/usr/bin/env python3
"""Generate sprites for Daimler Motor Bus (1898).

Single-deck (early horse-bus replacement)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="daimler_motor_bus",
    name='Daimler Motor Bus',
    year=1898,
    double_deck=False,
    body_length=0.55,
    primary=(30, 70, 40, 255),
    secondary=(20, 50, 28, 255),
    trim=(200, 190, 150, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

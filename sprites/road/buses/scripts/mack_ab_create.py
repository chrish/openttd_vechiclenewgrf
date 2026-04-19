#!/usr/bin/env python3
"""Generate sprites for Mack AB (1913).

Single-deck (early American city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mack_ab",
    name='Mack AB',
    year=1913,
    double_deck=False,
    body_length=0.75,
    primary=(30, 70, 40, 255),
    secondary=(20, 50, 28, 255),
    trim=(200, 190, 150, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz Lo 3500 (1930).

Single-deck (intercity coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_lo_3500",
    name='Mercedes-Benz Lo 3500',
    year=1930,
    double_deck=False,
    body_length=0.75,
    primary=(40, 45, 100, 255),
    secondary=(28, 30, 72, 255),
    trim=(190, 195, 225, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

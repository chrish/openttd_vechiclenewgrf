#!/usr/bin/env python3
"""Generate sprites for Volvo 7900 Electric (2015).

Single-deck (European electric city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volvo_7900_electric",
    name='Volvo 7900 Electric',
    year=2015,
    double_deck=False,
    body_length=0.8,
    primary=(50, 170, 80, 255),
    secondary=(35, 125, 58, 255),
    trim=(235, 250, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

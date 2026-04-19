#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 321 (1954).

Single-deck (German touring coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_321",
    name='Mercedes-Benz O 321',
    year=1954,
    double_deck=False,
    body_length=0.8,
    primary=(75, 35, 85, 255),
    secondary=(52, 24, 60, 255),
    trim=(215, 200, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

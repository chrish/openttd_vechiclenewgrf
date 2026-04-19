#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 10000 (1936).

Single-deck (German long-distance express)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_10000",
    name='Mercedes-Benz O 10000',
    year=1936,
    double_deck=False,
    body_length=0.8,
    primary=(165, 30, 30, 255),
    secondary=(120, 20, 20, 255),
    trim=(225, 205, 155, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

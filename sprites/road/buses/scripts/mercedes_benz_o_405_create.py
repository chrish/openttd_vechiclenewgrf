#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz O 405 (1987).

Single-deck (German standard city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_o_405",
    name='Mercedes-Benz O 405',
    year=1987,
    double_deck=False,
    body_length=0.8,
    primary=(35, 100, 160, 255),
    secondary=(25, 72, 115, 255),
    trim=(230, 240, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

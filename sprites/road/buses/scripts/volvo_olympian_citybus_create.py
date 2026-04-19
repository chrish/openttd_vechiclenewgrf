#!/usr/bin/env python3
"""Generate sprites for Volvo Olympian / Citybus (1985).

Double-deck (British/Asian cities)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volvo_olympian_citybus",
    name='Volvo Olympian / Citybus',
    year=1985,
    double_deck=True,
    body_length=0.9,
    primary=(140, 80, 40, 255),
    secondary=(100, 58, 28, 255),
    trim=(240, 230, 215, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

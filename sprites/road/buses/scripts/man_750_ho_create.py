#!/usr/bin/env python3
"""Generate sprites for MAN 750 HO (1964).

Single-deck (German standard city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="man_750_ho",
    name='MAN 750 HO',
    year=1964,
    double_deck=False,
    body_length=0.8,
    primary=(160, 50, 50, 255),
    secondary=(115, 35, 35, 255),
    trim=(240, 235, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

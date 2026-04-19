#!/usr/bin/env python3
"""Generate sprites for Guy Arab (1940).

Double-deck (British wartime utility bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="guy_arab",
    name='Guy Arab',
    year=1940,
    double_deck=True,
    body_length=0.85,
    primary=(155, 40, 40, 255),
    secondary=(110, 28, 28, 255),
    trim=(240, 225, 180, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

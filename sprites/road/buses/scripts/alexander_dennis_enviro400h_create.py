#!/usr/bin/env python3
"""Generate sprites for Alexander Dennis Enviro400H (2013).

Double-deck (hybrid British)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="alexander_dennis_enviro400h",
    name='Alexander Dennis Enviro400H',
    year=2013,
    double_deck=True,
    body_length=0.9,
    primary=(100, 50, 150, 255),
    secondary=(72, 35, 110, 255),
    trim=(235, 225, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Velaris V-1 Flicker (2095).

Personal hypercar (vacuum-tube hybrid, urban-to-city)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="velaris_v_1_flicker",
    name='Velaris V-1 Flicker',
    year=2095,
    double_deck=False,
    body_length=0.55,
    primary=(255, 180, 40, 255),
    secondary=(185, 130, 28, 255),
    trim=(252, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

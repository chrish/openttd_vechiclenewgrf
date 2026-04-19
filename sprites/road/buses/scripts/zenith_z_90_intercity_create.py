#!/usr/bin/env python3
"""Generate sprites for Zenith Z-90 InterCity (2034).

Double-deck electric coach (motorway express)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="zenith_z_90_intercity",
    name='Zenith Z-90 InterCity',
    year=2034,
    double_deck=True,
    body_length=0.9,
    primary=(30, 120, 190, 255),
    secondary=(20, 88, 140, 255),
    trim=(240, 245, 255, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Velaris V-200 CoachElite (2042).

Double-deck autonomous coach (intercity luxury)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="velaris_v_200_coachelite",
    name='Velaris V-200 CoachElite',
    year=2042,
    double_deck=True,
    body_length=0.95,
    primary=(200, 200, 210, 255),
    secondary=(150, 150, 158, 255),
    trim=(60, 200, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

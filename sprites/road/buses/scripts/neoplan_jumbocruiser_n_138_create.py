#!/usr/bin/env python3
"""Generate sprites for Neoplan Jumbocruiser N 138 (1981).

Double-deck articulated coach (largest bus ever)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="neoplan_jumbocruiser_n_138",
    name='Neoplan Jumbocruiser N 138',
    year=1981,
    double_deck=True,
    body_length=0.9,
    primary=(90, 90, 90, 255),
    secondary=(60, 60, 60, 255),
    trim=(220, 220, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Halcyon H-100 AeroCoach (2048).

Streamlined autonomous coach (dedicated motorway lanes)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="halcyon_h_100_aerocoach",
    name='Halcyon H-100 AeroCoach',
    year=2048,
    double_deck=False,
    body_length=0.9,
    primary=(220, 225, 235, 255),
    secondary=(170, 175, 185, 255),
    trim=(40, 180, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

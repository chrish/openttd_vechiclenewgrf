#!/usr/bin/env python3
"""Generate sprites for Volterra V-120 CityPulse (2030).

Single-deck electric (solid-state battery, fast-charge)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volterra_v_120_citypulse",
    name='Volterra V-120 CityPulse',
    year=2030,
    double_deck=False,
    body_length=0.9,
    primary=(60, 60, 65, 255),
    secondary=(42, 42, 46, 255),
    trim=(230, 230, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

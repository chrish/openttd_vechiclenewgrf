#!/usr/bin/env python3
"""Generate sprites for Solaris Sol-600 CityWorm (2055).

Modular road-train (6 detachable pods, urban trunk)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="solaris_sol_600_cityworm",
    name='Solaris Sol-600 CityWorm',
    year=2055,
    double_deck=False,
    body_length=0.95,
    primary=(180, 60, 200, 255),
    secondary=(130, 42, 145, 255),
    trim=(240, 230, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

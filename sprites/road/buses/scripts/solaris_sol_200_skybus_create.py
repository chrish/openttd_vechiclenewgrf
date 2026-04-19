#!/usr/bin/env python3
"""Generate sprites for Solaris Sol-200 SkyBus (2080).

Automated express coach (vacuum-tube compatible)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="solaris_sol_200_skybus",
    name='Solaris Sol-200 SkyBus',
    year=2080,
    double_deck=False,
    body_length=0.95,
    primary=(200, 200, 210, 255),
    secondary=(150, 150, 158, 255),
    trim=(60, 200, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

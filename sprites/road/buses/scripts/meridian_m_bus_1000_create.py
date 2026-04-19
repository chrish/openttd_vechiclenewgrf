#!/usr/bin/env python3
"""Generate sprites for Meridian M-Bus 1000 (2090).

Mega-bus (10-module, intercity corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="meridian_m_bus_1000",
    name='Meridian M-Bus 1000',
    year=2090,
    double_deck=False,
    body_length=0.95,
    primary=(50, 200, 120, 255),
    secondary=(35, 145, 88, 255),
    trim=(235, 252, 242, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

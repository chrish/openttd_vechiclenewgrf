#!/usr/bin/env python3
"""Generate sprites for Solaris Sol-Bus 800 (2062).

Mega-bus road-train (8 double-deck modules)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="solaris_sol_bus_800",
    name='Solaris Sol-Bus 800',
    year=2062,
    double_deck=True,
    body_length=0.95,
    primary=(255, 180, 40, 255),
    secondary=(185, 130, 28, 255),
    trim=(252, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

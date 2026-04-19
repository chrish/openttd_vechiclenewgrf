#!/usr/bin/env python3
"""Generate sprites for Halcyon H-10 Odyssey (2072).

Autonomous luxury liner (mobile living room)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="halcyon_h_10_odyssey",
    name='Halcyon H-10 Odyssey',
    year=2072,
    double_deck=False,
    body_length=0.55,
    primary=(180, 60, 200, 255),
    secondary=(130, 42, 145, 255),
    trim=(240, 230, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

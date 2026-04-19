#!/usr/bin/env python3
"""Generate sprites for Ikarus 260/280 (1970).

Single-deck / articulated (Eastern Bloc standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ikarus_260_280",
    name='Ikarus 260/280',
    year=1970,
    double_deck=False,
    body_length=0.95,
    primary=(200, 140, 30, 255),
    secondary=(145, 100, 20, 255),
    trim=(250, 245, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

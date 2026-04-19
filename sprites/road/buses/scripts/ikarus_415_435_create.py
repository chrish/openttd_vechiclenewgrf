#!/usr/bin/env python3
"""Generate sprites for Ikarus 415/435 (1982).

Single-deck / articulated (updated Eastern Bloc standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ikarus_415_435",
    name='Ikarus 415/435',
    year=1982,
    double_deck=False,
    body_length=0.95,
    primary=(160, 50, 50, 255),
    secondary=(115, 35, 35, 255),
    trim=(240, 235, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

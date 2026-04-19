#!/usr/bin/env python3
"""Generate sprites for Ikarus 30 (1951).

Single-deck (Hungarian city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ikarus_30",
    name='Ikarus 30',
    year=1951,
    double_deck=False,
    body_length=0.75,
    primary=(130, 100, 30, 255),
    secondary=(95, 72, 20, 255),
    trim=(230, 220, 170, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

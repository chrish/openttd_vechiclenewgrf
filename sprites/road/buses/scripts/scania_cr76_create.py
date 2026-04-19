#!/usr/bin/env python3
"""Generate sprites for Scania CR76 (1968).

Single-deck (Swedish city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="scania_cr76",
    name='Scania CR76',
    year=1968,
    double_deck=False,
    body_length=0.8,
    primary=(35, 100, 160, 255),
    secondary=(25, 72, 115, 255),
    trim=(230, 240, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

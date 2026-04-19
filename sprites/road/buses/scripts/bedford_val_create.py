#!/usr/bin/env python3
"""Generate sprites for Bedford VAL (1967).

Single-deck (British lightweight coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="bedford_val",
    name='Bedford VAL',
    year=1967,
    double_deck=False,
    body_length=0.8,
    primary=(180, 35, 35, 255),
    secondary=(130, 25, 25, 255),
    trim=(240, 240, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

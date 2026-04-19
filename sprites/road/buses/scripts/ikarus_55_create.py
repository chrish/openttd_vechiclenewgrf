#!/usr/bin/env python3
"""Generate sprites for Ikarus 55 (1958).

Single-deck (Hungarian export coach, "Facelift")
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ikarus_55",
    name='Ikarus 55',
    year=1958,
    double_deck=False,
    body_length=0.75,
    primary=(165, 30, 30, 255),
    secondary=(120, 20, 20, 255),
    trim=(225, 205, 155, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

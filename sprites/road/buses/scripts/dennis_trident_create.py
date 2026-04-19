#!/usr/bin/env python3
"""Generate sprites for Dennis Trident (1993).

Double-deck (Hong Kong / UK)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="dennis_trident",
    name='Dennis Trident',
    year=1993,
    double_deck=True,
    body_length=0.9,
    primary=(50, 80, 130, 255),
    secondary=(35, 58, 95, 255),
    trim=(225, 235, 245, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

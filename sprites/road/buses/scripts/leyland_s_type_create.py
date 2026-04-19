#!/usr/bin/env python3
"""Generate sprites for Leyland S-type (1908).

Single-deck (early British motor bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_s_type",
    name='Leyland S-type',
    year=1908,
    double_deck=False,
    body_length=0.75,
    primary=(45, 55, 70, 255),
    secondary=(30, 38, 50, 255),
    trim=(200, 210, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

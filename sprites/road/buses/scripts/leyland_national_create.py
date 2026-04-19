#!/usr/bin/env python3
"""Generate sprites for Leyland National (1973).

Single-deck (integral British city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_national",
    name='Leyland National',
    year=1973,
    double_deck=False,
    body_length=0.8,
    primary=(160, 50, 50, 255),
    secondary=(115, 35, 35, 255),
    trim=(240, 235, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

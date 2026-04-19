#!/usr/bin/env python3
"""Generate sprites for Irizar ie tram (2020).

Articulated (Spanish electric tram-bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="irizar_ie_tram",
    name='Irizar ie tram',
    year=2020,
    double_deck=False,
    body_length=0.95,
    primary=(100, 50, 150, 255),
    secondary=(72, 35, 110, 255),
    trim=(235, 225, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

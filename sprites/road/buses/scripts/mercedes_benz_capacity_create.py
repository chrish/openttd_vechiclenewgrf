#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz CapaCity (2004).

Bi-articulated (super-capacity urban bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_capacity",
    name='Mercedes-Benz CapaCity',
    year=2004,
    double_deck=False,
    body_length=0.95,
    primary=(240, 240, 245, 255),
    secondary=(195, 195, 200, 255),
    trim=(50, 50, 55, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

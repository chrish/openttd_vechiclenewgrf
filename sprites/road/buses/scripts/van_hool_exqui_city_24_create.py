#!/usr/bin/env python3
"""Generate sprites for Van Hool Exqui.City 24 (2016).

Bi-articulated (electric/trolleybus BRT)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="van_hool_exqui_city_24",
    name='Van Hool Exqui.City 24',
    year=2016,
    double_deck=False,
    body_length=0.95,
    primary=(200, 60, 60, 255),
    secondary=(145, 42, 42, 255),
    trim=(250, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

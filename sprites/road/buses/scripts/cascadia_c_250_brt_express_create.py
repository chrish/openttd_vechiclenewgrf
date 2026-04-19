#!/usr/bin/env python3
"""Generate sprites for Cascadia C-250 BRT Express (2033).

Bi-articulated electric (dedicated BRT corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="cascadia_c_250_brt_express",
    name='Cascadia C-250 BRT Express',
    year=2033,
    double_deck=False,
    body_length=0.95,
    primary=(30, 90, 120, 255),
    secondary=(20, 65, 88, 255),
    trim=(230, 240, 248, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

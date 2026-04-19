#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz eCitaro (2018).

Single-deck (production battery-electric)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_ecitaro",
    name='Mercedes-Benz eCitaro',
    year=2018,
    double_deck=False,
    body_length=0.8,
    primary=(60, 60, 65, 255),
    secondary=(42, 42, 46, 255),
    trim=(230, 230, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for ACF-Brill IC-41 (1949).

Single-deck (American intercity coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="acf_brill_ic_41",
    name='ACF-Brill IC-41',
    year=1949,
    double_deck=False,
    body_length=0.8,
    primary=(30, 90, 60, 255),
    secondary=(20, 65, 42, 255),
    trim=(200, 220, 190, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

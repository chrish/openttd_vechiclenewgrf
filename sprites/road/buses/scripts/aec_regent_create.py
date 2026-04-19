#!/usr/bin/env python3
"""Generate sprites for AEC Regent (1929).

Double-deck (iconic British double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_regent",
    name='AEC Regent',
    year=1929,
    double_deck=True,
    body_length=0.85,
    primary=(165, 30, 30, 255),
    secondary=(120, 20, 20, 255),
    trim=(225, 205, 155, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

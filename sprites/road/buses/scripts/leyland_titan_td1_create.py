#!/usr/bin/env python3
"""Generate sprites for Leyland Titan TD1 (1929).

Double-deck (British standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_titan_td1",
    name='Leyland Titan TD1',
    year=1929,
    double_deck=True,
    body_length=0.8,
    primary=(30, 90, 60, 255),
    secondary=(20, 65, 42, 255),
    trim=(200, 220, 190, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

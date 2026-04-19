#!/usr/bin/env python3
"""Generate sprites for AEC Regent III (RT) (1946).

Double-deck (London RT-type, iconic red bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_regent_iii",
    name='AEC Regent III (RT)',
    year=1946,
    double_deck=True,
    body_length=0.85,
    primary=(50, 70, 50, 255),
    secondary=(35, 50, 35, 255),
    trim=(200, 215, 195, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for AEC S-type (1921).

Double-deck (London General)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_s_type",
    name='AEC S-type',
    year=1921,
    double_deck=True,
    body_length=0.8,
    primary=(50, 60, 40, 255),
    secondary=(35, 42, 28, 255),
    trim=(195, 185, 150, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

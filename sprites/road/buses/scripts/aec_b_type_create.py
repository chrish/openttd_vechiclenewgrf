#!/usr/bin/env python3
"""Generate sprites for AEC B-type (1910).

Double-deck (iconic London General Omnibus, also WW1 transport)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_b_type",
    name='AEC B-type',
    year=1910,
    double_deck=True,
    body_length=0.75,
    primary=(130, 30, 30, 255),
    secondary=(95, 20, 20, 255),
    trim=(235, 215, 175, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

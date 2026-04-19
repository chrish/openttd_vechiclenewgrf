#!/usr/bin/env python3
"""Generate sprites for Setra S 431 DT TopClass (2000).

Double-deck coach (luxury touring)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="setra_s_431_dt_topclass",
    name='Setra S 431 DT TopClass',
    year=2000,
    double_deck=True,
    body_length=0.9,
    primary=(30, 90, 120, 255),
    secondary=(20, 65, 88, 255),
    trim=(230, 240, 248, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for GM "New Look" TDH-5303 (1965).

Single-deck (improved Fishbowl transit)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="gm_new_look_tdh_5303",
    name='GM "New Look" TDH-5303',
    year=1965,
    double_deck=False,
    body_length=0.8,
    primary=(50, 80, 130, 255),
    secondary=(35, 58, 95, 255),
    trim=(225, 235, 245, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

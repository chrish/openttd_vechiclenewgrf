#!/usr/bin/env python3
"""Generate sprites for GM TDH-3610 "Old Look" (1947).

Single-deck (American transit standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="gm_tdh_3610_old_look",
    name='GM TDH-3610 "Old Look"',
    year=1947,
    double_deck=False,
    body_length=0.8,
    primary=(140, 60, 30, 255),
    secondary=(100, 42, 20, 255),
    trim=(235, 215, 175, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

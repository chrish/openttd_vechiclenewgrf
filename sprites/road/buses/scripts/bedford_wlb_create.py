#!/usr/bin/env python3
"""Generate sprites for Bedford WLB (1932).

Single-deck (small British bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="bedford_wlb",
    name='Bedford WLB',
    year=1932,
    double_deck=False,
    body_length=0.65,
    primary=(90, 50, 30, 255),
    secondary=(65, 35, 20, 255),
    trim=(220, 200, 165, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

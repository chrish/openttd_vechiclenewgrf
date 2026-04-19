#!/usr/bin/env python3
"""Generate sprites for Ford Transit Bus (military) (1942).

Single-deck (wartime transport)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="ford_transit_bus",
    name='Ford Transit Bus (military)',
    year=1942,
    double_deck=False,
    body_length=0.75,
    primary=(90, 50, 30, 255),
    secondary=(65, 35, 20, 255),
    trim=(220, 200, 165, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

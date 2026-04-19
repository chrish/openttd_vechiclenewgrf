#!/usr/bin/env python3
"""Generate sprites for GM PD-3751 Silversides (1939).

Single-deck (iconic Greyhound intercity)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="gm_pd_3751_silversides",
    name='GM PD-3751 Silversides',
    year=1939,
    double_deck=False,
    body_length=0.8,
    primary=(130, 100, 30, 255),
    secondary=(95, 72, 20, 255),
    trim=(230, 220, 170, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

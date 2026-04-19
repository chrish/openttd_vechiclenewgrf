#!/usr/bin/env python3
"""Generate sprites for MCI MC-8 (1972).

Single-deck (North American intercity coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mci_mc_8",
    name='MCI MC-8',
    year=1972,
    double_deck=False,
    body_length=0.8,
    primary=(220, 220, 220, 255),
    secondary=(180, 180, 180, 255),
    trim=(60, 60, 60, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

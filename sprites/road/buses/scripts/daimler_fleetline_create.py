#!/usr/bin/env python3
"""Generate sprites for Daimler Fleetline (1963).

Double-deck (rear-engine British double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="daimler_fleetline",
    name='Daimler Fleetline',
    year=1963,
    double_deck=True,
    body_length=0.85,
    primary=(220, 220, 220, 255),
    secondary=(180, 180, 180, 255),
    trim=(60, 60, 60, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

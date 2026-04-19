#!/usr/bin/env python3
"""Generate sprites for Horizon H-60 Shuttle (2032).

Single-deck autonomous (Level 5 self-driving)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="horizon_h_60_shuttle",
    name='Horizon H-60 Shuttle',
    year=2032,
    double_deck=False,
    body_length=0.85,
    primary=(100, 50, 150, 255),
    secondary=(72, 35, 110, 255),
    trim=(235, 225, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

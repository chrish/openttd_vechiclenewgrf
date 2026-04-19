#!/usr/bin/env python3
"""Generate sprites for Leyland Titan PD2 (1946).

Double-deck (post-war British standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_titan_pd2",
    name='Leyland Titan PD2',
    year=1946,
    double_deck=True,
    body_length=0.85,
    primary=(75, 35, 85, 255),
    secondary=(52, 24, 60, 255),
    trim=(215, 200, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

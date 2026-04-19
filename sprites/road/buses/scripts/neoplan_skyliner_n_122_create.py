#!/usr/bin/env python3
"""Generate sprites for Neoplan Skyliner N 122 (1971).

Double-deck coach (first modern three-axle coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="neoplan_skyliner_n_122",
    name='Neoplan Skyliner N 122',
    year=1971,
    double_deck=True,
    body_length=0.85,
    primary=(90, 90, 90, 255),
    secondary=(60, 60, 60, 255),
    trim=(220, 220, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

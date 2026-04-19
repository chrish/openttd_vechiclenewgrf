#!/usr/bin/env python3
"""Generate sprites for Leyland N-type (1920).

Single-deck (post-WW1 British bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_n_type",
    name='Leyland N-type',
    year=1920,
    double_deck=False,
    body_length=0.75,
    primary=(100, 28, 28, 255),
    secondary=(70, 18, 18, 255),
    trim=(220, 200, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

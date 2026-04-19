#!/usr/bin/env python3
"""Generate sprites for Citroën T45 (1932).

Single-deck (French city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="citron_t45",
    name='Citroën T45',
    year=1932,
    double_deck=False,
    body_length=0.75,
    primary=(75, 35, 85, 255),
    secondary=(52, 24, 60, 255),
    trim=(215, 200, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

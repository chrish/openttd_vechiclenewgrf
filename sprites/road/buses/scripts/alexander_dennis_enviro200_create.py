#!/usr/bin/env python3
"""Generate sprites for Alexander Dennis Enviro200 (2003).

Single-deck (British midibus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="alexander_dennis_enviro200",
    name='Alexander Dennis Enviro200',
    year=2003,
    double_deck=False,
    body_length=0.8,
    primary=(200, 60, 60, 255),
    secondary=(145, 42, 42, 255),
    trim=(250, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

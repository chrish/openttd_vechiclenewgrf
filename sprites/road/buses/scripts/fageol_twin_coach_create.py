#!/usr/bin/env python3
"""Generate sprites for Fageol Twin Coach (1925).

Single-deck (twin-engine, American transit)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="fageol_twin_coach",
    name='Fageol Twin Coach',
    year=1925,
    double_deck=False,
    body_length=0.8,
    primary=(90, 50, 30, 255),
    secondary=(65, 35, 20, 255),
    trim=(220, 200, 165, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

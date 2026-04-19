#!/usr/bin/env python3
"""Generate sprites for Titan T-2000 GlobalHaul (2080).

Mega-train autonomous (transcontinental freight corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="titan_t_2000_globalhaul",
    name='Titan T-2000 GlobalHaul',
    year=2080,
    double_deck=False,
    body_length=0.95,
    primary=(80, 50, 160, 255),
    secondary=(58, 35, 115, 255),
    trim=(210, 200, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

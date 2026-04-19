#!/usr/bin/env python3
"""Generate sprites for Meridian M-180 MetroLink (2031).

Articulated electric (inductive road charging)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="meridian_m_180_metrolink",
    name='Meridian M-180 MetroLink',
    year=2031,
    double_deck=False,
    body_length=0.95,
    primary=(180, 130, 40, 255),
    secondary=(130, 95, 28, 255),
    trim=(250, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

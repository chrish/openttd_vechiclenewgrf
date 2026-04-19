#!/usr/bin/env python3
"""Generate sprites for Benz Omnibus (1895).

Single-deck (first motor bus service, Siegerland)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="benz_omnibus",
    name='Benz Omnibus',
    year=1895,
    double_deck=False,
    body_length=0.55,
    primary=(130, 30, 30, 255),
    secondary=(95, 20, 20, 255),
    trim=(235, 215, 175, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

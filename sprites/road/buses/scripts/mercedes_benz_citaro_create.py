#!/usr/bin/env python3
"""Generate sprites for Mercedes-Benz Citaro (O 530) (1995).

Single-deck (most successful European city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mercedes_benz_citaro",
    name='Mercedes-Benz Citaro (O 530)',
    year=1995,
    double_deck=False,
    body_length=0.8,
    primary=(140, 80, 40, 255),
    secondary=(100, 58, 28, 255),
    trim=(240, 230, 215, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

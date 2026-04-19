#!/usr/bin/env python3
"""Generate sprites for Saurer Alpenwagen (1952).

Single-deck (Swiss alpine postbus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="saurer_alpenwagen",
    name='Saurer Alpenwagen',
    year=1952,
    double_deck=False,
    body_length=0.8,
    primary=(155, 40, 40, 255),
    secondary=(110, 28, 28, 255),
    trim=(240, 225, 180, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Neoplan Starliner N 516 (1994).

Single-deck (luxury touring coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="neoplan_starliner_n_516",
    name='Neoplan Starliner N 516',
    year=1994,
    double_deck=False,
    body_length=0.8,
    primary=(35, 110, 100, 255),
    secondary=(25, 80, 72, 255),
    trim=(225, 245, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

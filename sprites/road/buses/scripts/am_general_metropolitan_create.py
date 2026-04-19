#!/usr/bin/env python3
"""Generate sprites for AM General Metropolitan (1978).

Single-deck (American transit)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="am_general_metropolitan",
    name='AM General Metropolitan',
    year=1978,
    double_deck=False,
    body_length=0.8,
    primary=(40, 130, 70, 255),
    secondary=(28, 95, 50, 255),
    trim=(230, 245, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

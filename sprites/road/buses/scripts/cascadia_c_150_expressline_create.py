#!/usr/bin/env python3
"""Generate sprites for Cascadia C-150 ExpressLine (2075).

Autonomous express bus (dedicated highway lane)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="cascadia_c_150_expressline",
    name='Cascadia C-150 ExpressLine',
    year=2075,
    double_deck=False,
    body_length=0.95,
    primary=(255, 180, 40, 255),
    secondary=(185, 130, 28, 255),
    trim=(252, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

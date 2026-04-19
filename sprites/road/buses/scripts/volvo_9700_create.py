#!/usr/bin/env python3
"""Generate sprites for Volvo 9700 (2005).

Single-deck (touring/express coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volvo_9700",
    name='Volvo 9700',
    year=2005,
    double_deck=False,
    body_length=0.8,
    primary=(60, 60, 65, 255),
    secondary=(42, 42, 46, 255),
    trim=(230, 230, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

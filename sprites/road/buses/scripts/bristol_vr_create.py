#!/usr/bin/env python3
"""Generate sprites for Bristol VR (1969).

Double-deck (rear-engine British)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="bristol_vr",
    name='Bristol VR',
    year=1969,
    double_deck=True,
    body_length=0.85,
    primary=(40, 130, 70, 255),
    secondary=(28, 95, 50, 255),
    trim=(230, 245, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

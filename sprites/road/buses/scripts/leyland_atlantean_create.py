#!/usr/bin/env python3
"""Generate sprites for Leyland Atlantean (1961).

Double-deck (first rear-engine double-decker)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="leyland_atlantean",
    name='Leyland Atlantean',
    year=1961,
    double_deck=True,
    body_length=0.85,
    primary=(200, 140, 30, 255),
    secondary=(145, 100, 20, 255),
    trim=(250, 245, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Scania OmniExpress (2007).

Single-deck (Scandinavian express coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="scania_omniexpress",
    name='Scania OmniExpress',
    year=2007,
    double_deck=False,
    body_length=0.8,
    primary=(30, 120, 190, 255),
    secondary=(20, 88, 140, 255),
    trim=(240, 245, 255, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

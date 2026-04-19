#!/usr/bin/env python3
"""Generate sprites for Alexander Dennis Enviro400EV (2019).

Double-deck (battery-electric British)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="alexander_dennis_enviro400ev",
    name='Alexander Dennis Enviro400EV',
    year=2019,
    double_deck=True,
    body_length=0.9,
    primary=(180, 130, 40, 255),
    secondary=(130, 95, 28, 255),
    trim=(250, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Velaris V-6 Aura (2065).

Autonomous car (ambient AI, self-healing materials)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="velaris_v_6_aura",
    name='Velaris V-6 Aura',
    year=2065,
    double_deck=False,
    body_length=0.55,
    primary=(200, 200, 210, 255),
    secondary=(150, 150, 158, 255),
    trim=(60, 200, 160, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

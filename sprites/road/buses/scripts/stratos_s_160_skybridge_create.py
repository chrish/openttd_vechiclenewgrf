#!/usr/bin/env python3
"""Generate sprites for Stratos S-160 SkyBridge (2037).

Articulated autonomous (elevated guideway compatible)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="stratos_s_160_skybridge",
    name='Stratos S-160 SkyBridge',
    year=2037,
    double_deck=False,
    body_length=0.95,
    primary=(50, 200, 120, 255),
    secondary=(35, 145, 88, 255),
    trim=(235, 252, 242, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

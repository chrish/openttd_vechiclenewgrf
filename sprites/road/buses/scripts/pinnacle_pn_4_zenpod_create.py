#!/usr/bin/env python3
"""Generate sprites for Pinnacle PN-4 ZenPod (2085).

Autonomous pod (personalized AI, any-terrain)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="pinnacle_pn_4_zenpod",
    name='Pinnacle PN-4 ZenPod',
    year=2085,
    double_deck=False,
    body_length=0.55,
    primary=(220, 225, 235, 255),
    secondary=(170, 175, 185, 255),
    trim=(40, 180, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

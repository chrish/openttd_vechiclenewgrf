#!/usr/bin/env python3
"""Generate sprites for Pinnacle PN-45 RapidPod (2038).

Short autonomous shuttle (last-mile + express)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="pinnacle_pn_45_rapidpod",
    name='Pinnacle PN-45 RapidPod',
    year=2038,
    double_deck=False,
    body_length=0.8,
    primary=(255, 180, 40, 255),
    secondary=(185, 130, 28, 255),
    trim=(252, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

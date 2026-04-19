#!/usr/bin/env python3
"""Generate sprites for Titan T-1000 OreCarrier (2065).

Autonomous mega-hauler (dedicated mining corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="titan_t_1000_orecarrier",
    name='Titan T-1000 OreCarrier',
    year=2065,
    double_deck=False,
    body_length=0.95,
    primary=(60, 70, 90, 255),
    secondary=(42, 50, 65, 255),
    trim=(200, 210, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

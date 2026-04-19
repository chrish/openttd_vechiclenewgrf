#!/usr/bin/env python3
"""Generate sprites for Yutong ZK6125CHEVPG (2010).

Single-deck (Chinese hybrid city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="yutong_zk6125chevpg",
    name='Yutong ZK6125CHEVPG',
    year=2010,
    double_deck=False,
    body_length=0.85,
    primary=(240, 240, 245, 255),
    secondary=(195, 195, 200, 255),
    trim=(50, 50, 55, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

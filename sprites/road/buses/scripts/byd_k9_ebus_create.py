#!/usr/bin/env python3
"""Generate sprites for BYD K9 / ebus (2012).

Single-deck (Chinese electric city bus, global export)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="byd_k9_ebus",
    name='BYD K9 / ebus',
    year=2012,
    double_deck=False,
    body_length=0.85,
    primary=(180, 130, 40, 255),
    secondary=(130, 95, 28, 255),
    trim=(250, 248, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

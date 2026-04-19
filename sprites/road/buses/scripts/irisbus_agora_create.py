#!/usr/bin/env python3
"""Generate sprites for Irisbus Agora (1997).

Single-deck (French standard city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="irisbus_agora",
    name='Irisbus Agora',
    year=1997,
    double_deck=False,
    body_length=0.8,
    primary=(40, 130, 70, 255),
    secondary=(28, 95, 50, 255),
    trim=(230, 245, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Proterra Catalyst E2 (2017).

Single-deck (American battery-electric transit)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="proterra_catalyst_e2",
    name='Proterra Catalyst E2',
    year=2017,
    double_deck=False,
    body_length=0.8,
    primary=(240, 240, 245, 255),
    secondary=(195, 195, 200, 255),
    trim=(50, 50, 55, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

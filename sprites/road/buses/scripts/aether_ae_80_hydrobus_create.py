#!/usr/bin/env python3
"""Generate sprites for Aether AE-80 HydroBus (2036).

Single-deck hydrogen fuel cell (long-range rural)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aether_ae_80_hydrobus",
    name='Aether AE-80 HydroBus',
    year=2036,
    double_deck=False,
    body_length=0.85,
    primary=(180, 60, 200, 255),
    secondary=(130, 42, 145, 255),
    trim=(240, 230, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

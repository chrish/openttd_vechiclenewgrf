#!/usr/bin/env python3
"""Generate sprites for MAN SL 200 (1974).

Single-deck (German standard city bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="man_sl_200",
    name='MAN SL 200',
    year=1974,
    double_deck=False,
    body_length=0.8,
    primary=(50, 80, 130, 255),
    secondary=(35, 58, 95, 255),
    trim=(225, 235, 245, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

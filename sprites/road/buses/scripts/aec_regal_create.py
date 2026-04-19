#!/usr/bin/env python3
"""Generate sprites for AEC Regal (1931).

Single-deck (British coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="aec_regal",
    name='AEC Regal',
    year=1931,
    double_deck=False,
    body_length=0.75,
    primary=(155, 40, 40, 255),
    secondary=(110, 28, 28, 255),
    trim=(240, 225, 180, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

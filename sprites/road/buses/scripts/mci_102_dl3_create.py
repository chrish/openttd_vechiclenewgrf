#!/usr/bin/env python3
"""Generate sprites for MCI 102-DL3 (1988).

Single-deck (North American intercity)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="mci_102_dl3",
    name='MCI 102-DL3',
    year=1988,
    double_deck=False,
    body_length=0.8,
    primary=(40, 130, 70, 255),
    secondary=(28, 95, 50, 255),
    trim=(230, 245, 235, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

#!/usr/bin/env python3
"""Generate sprites for Pickwick Nite Coach (1931).

Single-deck (American sleeper coach)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="pickwick_nite_coach",
    name='Pickwick Nite Coach',
    year=1931,
    double_deck=False,
    body_length=0.75,
    primary=(45, 80, 90, 255),
    secondary=(30, 58, 65, 255),
    trim=(195, 215, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

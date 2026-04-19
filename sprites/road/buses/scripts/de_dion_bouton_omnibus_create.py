#!/usr/bin/env python3
"""Generate sprites for De Dion-Bouton Omnibus (1905).

Single-deck (French motor bus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="de_dion_bouton_omnibus",
    name='De Dion-Bouton Omnibus',
    year=1905,
    double_deck=False,
    body_length=0.65,
    primary=(50, 60, 40, 255),
    secondary=(35, 42, 28, 255),
    trim=(195, 185, 150, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

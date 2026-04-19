#!/usr/bin/env python3
"""Generate sprites for Colossus C-5000 Leviathan (2085).

Industrial mega-hauler (continental mining, guided corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="colossus_c_5000_leviathan",
    name='Colossus C-5000 Leviathan',
    year=2085,
    double_deck=False,
    body_length=0.95,
    primary=(40, 180, 220, 255),
    secondary=(28, 130, 160, 255),
    trim=(240, 245, 252, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

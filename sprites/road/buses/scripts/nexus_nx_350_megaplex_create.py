#!/usr/bin/env python3
"""Generate sprites for Nexus NX-350 MegaPlex (2050).

Tri-articulated autonomous (supercapacitor rapid-charge)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="nexus_nx_350_megaplex",
    name='Nexus NX-350 MegaPlex',
    year=2050,
    double_deck=False,
    body_length=0.95,
    primary=(40, 180, 220, 255),
    secondary=(28, 130, 160, 255),
    trim=(240, 245, 252, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

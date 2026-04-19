#!/usr/bin/env python3
"""Generate sprites for Quantum QT-X Infinity (2100).

Autonomous luxury (zero energy cost, ambient harvesting)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="quantum_qt_x_infinity",
    name='Quantum QT-X Infinity',
    year=2100,
    double_deck=False,
    body_length=0.55,
    primary=(60, 70, 90, 255),
    secondary=(42, 50, 65, 255),
    trim=(200, 210, 230, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

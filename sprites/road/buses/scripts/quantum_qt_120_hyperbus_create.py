#!/usr/bin/env python3
"""Generate sprites for Quantum QT-120 HyperBus (2060).

Closed-guideway electric (dedicated hyperbus lanes)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="quantum_qt_120_hyperbus",
    name='Quantum QT-120 HyperBus',
    year=2060,
    double_deck=False,
    body_length=0.9,
    primary=(50, 200, 120, 255),
    secondary=(35, 145, 88, 255),
    trim=(235, 252, 242, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

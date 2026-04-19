#!/usr/bin/env python3
"""Generate sprites for Quantum QT-1000 FreightNet (2075).

Autonomous mega-freight (modular, dedicated corridor)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="quantum_qt_1000_freightnet",
    name='Quantum QT-1000 FreightNet',
    year=2075,
    double_deck=False,
    body_length=0.95,
    primary=(50, 200, 120, 255),
    secondary=(35, 145, 88, 255),
    trim=(235, 252, 242, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

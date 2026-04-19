#!/usr/bin/env python3
"""Generate sprites for Dennis Dart (1986).

Single-deck (British midibus)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="dennis_dart",
    name='Dennis Dart',
    year=1986,
    double_deck=False,
    body_length=0.8,
    primary=(180, 35, 35, 255),
    secondary=(130, 25, 25, 255),
    trim=(240, 240, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

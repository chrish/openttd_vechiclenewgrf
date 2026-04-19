#!/usr/bin/env python3
"""Generate sprites for Volvo B58 / Ailsa B55 (1976).

Single-deck / double-deck (Swedish chassis)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="volvo_b58_ailsa_b55",
    name='Volvo B58 / Ailsa B55',
    year=1976,
    double_deck=True,
    body_length=0.85,
    primary=(180, 35, 35, 255),
    secondary=(130, 25, 25, 255),
    trim=(240, 240, 240, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

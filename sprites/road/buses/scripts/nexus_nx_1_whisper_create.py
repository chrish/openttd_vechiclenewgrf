#!/usr/bin/env python3
"""Generate sprites for Nexus NX-1 Whisper (2090).

Personal autonomous pod (weightless suspension feel)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="nexus_nx_1_whisper",
    name='Nexus NX-1 Whisper',
    year=2090,
    double_deck=False,
    body_length=0.55,
    primary=(180, 60, 200, 255),
    secondary=(130, 42, 145, 255),
    trim=(240, 230, 250, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

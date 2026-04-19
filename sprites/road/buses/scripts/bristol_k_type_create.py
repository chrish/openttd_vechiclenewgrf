#!/usr/bin/env python3
"""Generate sprites for Bristol K-type (1940).

Double-deck (British wartime/post-war standard)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="bristol_k_type",
    name='Bristol K-type',
    year=1940,
    double_deck=True,
    body_length=0.85,
    primary=(45, 80, 90, 255),
    secondary=(30, 58, 65, 255),
    trim=(195, 215, 220, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

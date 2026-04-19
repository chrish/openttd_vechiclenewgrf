#!/usr/bin/env python3
"""Generate sprites for GM Yellow Coach TG-3201 (1937).

Single-deck (streamlined Greyhound Silversides prototype)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bus_base import BusStyle, generate_bus_sprites

style = BusStyle(
    slug="gm_yellow_coach_tg_3201",
    name='GM Yellow Coach TG-3201',
    year=1937,
    double_deck=False,
    body_length=0.8,
    primary=(30, 90, 60, 255),
    secondary=(20, 65, 42, 255),
    trim=(200, 220, 190, 255),
)

if __name__ == "__main__":
    generate_bus_sprites(style, Path(__file__).resolve().parent.parent / "output")

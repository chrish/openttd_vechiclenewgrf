#!/usr/bin/env python3
"""Base drawing module for bus sprites.

Provides parameterized drawing functions that generate 32bpp sprite sheets
for OpenTTD buses across all eras (1895–2100+).

Usage:
    from bus_base import BusStyle, generate_bus_sprites

    style = BusStyle(slug="my_bus", name="My Bus", year=1925, ...)
    generate_bus_sprites(style, output_dir=Path("."))
"""

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw
import math

# ── Constants ─────────────────────────────────────────────────────────

RGBA = tuple[int, int, int, int]
TRANSPARENT = (0, 0, 0, 0)

# Sprite positions at 4x zoom (from templates.nml)
VIEWS_4X = [
    ("N",   0,   0,  32, 72),
    ("NE", 64,   0,  80, 76),
    ("E", 192,   0, 112, 60),
    ("SE", 384,  0,  80, 76),
    ("S",  512,  0,  32, 72),
    ("SW", 576,  0,  80, 76),
    ("W",  704,  0, 112, 60),
    ("NW", 896,  0,  80, 76),
]
SHEET_W_4X = 1008
SHEET_H_4X = 80

# Common fixed colors
BLACK      = (25, 25, 25, 255)
DARK_GREY  = (55, 55, 55, 255)
MED_GREY   = (90, 90, 90, 255)
LIGHT_GREY = (140, 140, 140, 255)
GLASS      = (160, 190, 210, 200)
GLASS_DARK = (120, 150, 170, 200)
FRAME      = (200, 180, 140, 255)
GOLD       = (195, 165, 75, 255)
RED_LIGHT  = (200, 40, 40, 255)
HEAD_LIGHT = (255, 240, 200, 255)
SHADOW     = (0, 0, 0, 40)
WOOD       = (110, 75, 35, 255)


# ── BusStyle ──────────────────────────────────────────────────────────

def _era(year: int) -> str:
    if year < 1925: return "early"
    if year < 1960: return "classic"
    if year < 2000: return "modern"
    if year < 2035: return "contemporary"
    return "futuristic"


@dataclass
class BusStyle:
    """Visual parameters for a bus sprite."""
    slug: str
    name: str
    year: int
    double_deck: bool = False
    body_length: float = 0.8
    primary: RGBA = (130, 30, 30, 255)
    secondary: RGBA = (95, 20, 20, 255)
    trim: RGBA = (235, 215, 175, 255)
    roof: RGBA = (60, 60, 60, 255)
    chassis_color: RGBA = (40, 35, 30, 255)

    @property
    def era(self) -> str:
        return _era(self.year)

    @property
    def lighter(self) -> RGBA:
        r, g, b, a = self.primary
        return (min(255, r + 30), min(255, g + 15), min(255, b + 15), a)

    @property
    def darker(self) -> RGBA:
        r, g, b, a = self.primary
        return (max(0, r - 25), max(0, g - 15), max(0, b - 15), a)


# ── Helper drawing functions ──────────────────────────────────────────

def _draw_wheel(d: ImageDraw.Draw, cx: int, cy: int, r: int,
                style: str = "solid"):
    """Draw a wheel at center (cx, cy) with radius r."""
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BLACK, outline=DARK_GREY)
    if style == "spoked" and r >= 5:
        ri = max(1, r - 3)
        d.ellipse([cx-ri, cy-ri, cx+ri, cy+ri],
                  fill=(60, 50, 35, 255), outline=(90, 80, 60, 255))
        rh = max(1, r // 3)
        d.ellipse([cx-rh, cy-rh, cx+rh, cy+rh], fill=(100, 90, 70, 255))
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            sx = int(cx + (ri - 1) * math.cos(rad))
            sy = int(cy + (ri - 1) * math.sin(rad))
            d.line([(cx, cy), (sx, sy)], fill=(90, 80, 60, 255), width=1)
    else:
        ri = max(1, r - 2)
        d.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=DARK_GREY)
        rh = max(1, r // 3)
        d.ellipse([cx-rh, cy-rh, cx+rh, cy+rh], fill=MED_GREY)


def _wheel_params(era: str):
    """Return (wheel_radius, wheel_style) for an era."""
    if era == "early":    return 8, "spoked"
    if era == "classic":  return 6, "spoked"
    return 5, "solid"


def _window_params(era: str):
    """Return (win_width, win_gap) for an era at 4x."""
    if era == "early":         return 7, 4
    if era == "classic":       return 8, 3
    if era == "modern":        return 9, 2
    if era == "contemporary":  return 10, 2
    return 12, 1  # futuristic


def _body_rect(s: BusStyle, ox: int, oy: int, w: int, h: int):
    """Compute body dimensions for E/W (side) view at 4x."""
    shadow_h = 6
    wheel_r, _ = _wheel_params(s.era)
    ground_y = oy + h - shadow_h
    chassis_h = 4 if s.era == "early" else 3
    body_bottom = ground_y - wheel_r + 2 - chassis_h

    margin = 8
    avail = w - margin * 2
    body_w = int(avail * s.body_length)

    if s.era == "early":
        bonnet = int(body_w * 0.15)
        body_left = ox + margin + bonnet
        body_right = body_left + body_w - bonnet
    elif s.era == "classic":
        bonnet = int(body_w * 0.08)
        body_left = ox + margin + bonnet
        body_right = body_left + body_w - bonnet
    else:
        bonnet = 0
        body_left = ox + margin + (avail - body_w) // 2
        body_right = body_left + body_w

    if s.double_deck:
        body_top = oy + 4
    elif s.era == "early":
        body_top = oy + int(h * 0.32)
    elif s.era == "futuristic":
        body_top = oy + int(h * 0.20)
    else:
        body_top = oy + int(h * 0.25)

    return {
        "ground_y": ground_y, "wheel_r": wheel_r, "chassis_h": chassis_h,
        "body_left": body_left, "body_right": body_right,
        "body_top": body_top, "body_bottom": body_bottom,
        "bonnet": bonnet, "margin": margin,
    }


def _draw_windows(d: ImageDraw.Draw, left: int, right: int,
                  top: int, bot: int, era: str, has_door: bool = False):
    """Draw a row of equally-spaced windows."""
    win_w, gap = _window_params(era)
    margin = 8
    door_zone = right - margin - win_w - 2 if has_door else -999

    x = left + margin
    while x + win_w <= right - margin:
        if has_door and door_zone - 2 <= x <= door_zone + win_w + 2:
            # Door
            d.rectangle([x, top, x + win_w, bot + 4], fill=GLASS_DARK)
            d.rectangle([x, top, x + win_w, bot + 4], outline=FRAME)
            d.rectangle([x + win_w - 2, (top + bot) // 2,
                         x + win_w - 1, (top + bot) // 2 + 2],
                        fill=LIGHT_GREY)
            x += win_w + gap
            continue
        d.rectangle([x, top, x + win_w, bot], fill=GLASS)
        if era in ("early", "classic"):
            d.rectangle([x, top, x + win_w, bot], outline=FRAME)
        x += win_w + gap


# ── E (east / side) view ─────────────────────────────────────────────

def _draw_east(img: Image.Image, s: BusStyle, ox: int, oy: int,
               w: int, h: int):
    d = ImageDraw.Draw(img)
    b = _body_rect(s, ox, oy, w, h)
    bl, br = b["body_left"], b["body_right"]
    bt, bb = b["body_top"], b["body_bottom"]
    gy = b["ground_y"]
    wr = b["wheel_r"]
    _, wstyle = _wheel_params(s.era)

    # Shadow
    d.rectangle([bl - 4, gy, br + 4, oy + h - 1], fill=SHADOW)

    # Chassis
    d.rectangle([bl - 2, bb, br + 2, bb + b["chassis_h"]], fill=s.chassis_color)

    # Wheels
    fw_x = bl + int((br - bl) * 0.15)
    rw_x = bl + int((br - bl) * 0.85)
    _draw_wheel(d, fw_x, gy - wr, wr, wstyle)
    _draw_wheel(d, rw_x, gy - wr, wr, wstyle)

    # Body
    if s.era == "futuristic":
        d.rounded_rectangle([bl, bt, br, bb], radius=8, fill=s.primary)
        d.rounded_rectangle([bl, bt, br, bb], radius=8, outline=s.secondary)
    elif s.era == "contemporary":
        d.rounded_rectangle([bl, bt, br, bb], radius=4, fill=s.primary)
    else:
        d.rectangle([bl, bt, br, bb], fill=s.primary)

    # Trim lines
    d.line([(bl, bt), (br, bt)], fill=s.trim, width=1)
    d.line([(bl, bb), (br, bb)], fill=s.secondary, width=1)
    if s.era in ("early", "classic"):
        waist = bt + (bb - bt) // 2
        d.line([(bl, waist), (br, waist)], fill=s.trim, width=1)

    # Double-deck handling
    if s.double_deck:
        deck_div = bt + (bb - bt) // 2 + 2
        # Upper deck body (lighter shade)
        d.rectangle([bl, bt, br, deck_div], fill=s.lighter)
        d.line([(bl, deck_div), (br, deck_div)], fill=s.trim, width=1)

        if s.era == "early":
            # Open top with railings
            rail_top = bt + 2
            for px in range(bl + 4, br - 4, 12):
                d.line([(px, rail_top), (px, deck_div)], fill=DARK_GREY, width=1)
            d.line([(bl + 4, rail_top), (br - 4, rail_top)],
                   fill=MED_GREY, width=1)
            for sx in range(bl + 6, br - 8, 10):
                d.rectangle([sx, deck_div - 4, sx + 5, deck_div - 1],
                            fill=WOOD)
        else:
            # Enclosed upper windows
            _draw_windows(d, bl, br, bt + 3, deck_div - 3, s.era)

        # Lower deck windows
        _draw_windows(d, bl, br, deck_div + 3, bb - 4, s.era, has_door=True)
    else:
        # Single-deck windows
        if s.era in ("early", "classic"):
            wt = bt + 4
            wb = bt + (bb - bt) // 2 - 1
        else:
            wt = bt + 3
            wb = bb - 4
        _draw_windows(d, bl, br, wt, wb, s.era, has_door=True)

    # Roof
    if not (s.double_deck and s.era == "early"):
        rt = bt - 2
        if rt >= oy:
            if s.era == "futuristic":
                d.rounded_rectangle([bl + 2, rt, br - 2, bt], radius=3,
                                    fill=s.roof)
            else:
                d.rectangle([bl + 2, rt, br - 2, bt], fill=s.roof)

    # Bonnet (early / classic)
    if s.era == "early" and b["bonnet"] > 0:
        bx = ox + b["margin"]
        d.rectangle([bx, bt + 6, bl, bb], fill=s.secondary)
        d.rectangle([bx, bt + 8, bx + 3, bb - 2], fill=LIGHT_GREY)
        d.ellipse([bx - 2, bt + 10, bx + 3, bt + 15],
                  fill=GOLD, outline=DARK_GREY)
    elif s.era == "classic" and b["bonnet"] > 0:
        bx = ox + b["margin"]
        d.rectangle([bx, bt + 3, bl, bb], fill=s.secondary)
        d.rectangle([bx, bt + 4, bx + 2, bb - 2], fill=LIGHT_GREY)

    # Headlights (modern+)
    if s.era in ("modern", "contemporary", "futuristic"):
        hl_y = bb - 6
        d.rectangle([bl, hl_y, bl + 3, hl_y + 3], fill=HEAD_LIGHT,
                    outline=LIGHT_GREY)

    # Tail light
    d.rectangle([br - 2, bb - 5, br, bb - 2], fill=RED_LIGHT)

    # Destination board
    if s.era != "futuristic":
        db_y = bt - 3 if s.double_deck and s.era != "early" else bt - 2
        if db_y >= oy:
            d.rectangle([bl + 3, db_y, bl + 18, db_y + 3], fill=s.trim)


# ── W (west) view — mirror of E ──────────────────────────────────────

def _draw_west(img: Image.Image, s: BusStyle, ox: int, oy: int,
               w: int, h: int):
    temp = Image.new("RGBA", (w, h), TRANSPARENT)
    _draw_east(temp, s, 0, 0, w, h)
    temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(temp, (ox, oy), temp)


# ── N (rear / heading away) view ─────────────────────────────────────

def _draw_north(img: Image.Image, s: BusStyle, ox: int, oy: int,
                w: int, h: int):
    d = ImageDraw.Draw(img)
    era = s.era
    wr, wstyle = _wheel_params(era)

    shadow_h = 5
    gy = oy + h - shadow_h
    d.rectangle([ox + 4, gy, ox + w - 4, oy + h - 1], fill=SHADOW)

    # Wheels
    _draw_wheel(d, ox + 6, gy - wr + 2, min(wr, 5), wstyle)
    _draw_wheel(d, ox + w - 6, gy - wr + 2, min(wr, 5), wstyle)

    # Chassis
    ch = 3
    ch_y = gy - wr - ch + 2
    d.rectangle([ox + 3, ch_y, ox + w - 3, ch_y + ch], fill=s.chassis_color)

    # Body
    bl = ox + 2
    br = ox + w - 2
    bb = ch_y
    bt = oy + (8 if s.double_deck else int(h * 0.30))

    if era == "futuristic":
        d.rounded_rectangle([bl, bt, br, bb], radius=4, fill=s.primary)
    else:
        d.rectangle([bl, bt, br, bb], fill=s.primary)

    d.line([(bl, bt), (br, bt)], fill=s.trim, width=1)
    d.line([(bl, bt + 1), (br, bt + 1)], fill=s.trim, width=1)

    if s.double_deck:
        deck_div = bt + (bb - bt) // 2 + 2
        d.rectangle([bl, bt, br, deck_div], fill=s.lighter)
        d.line([(bl, deck_div), (br, deck_div)], fill=s.trim, width=1)

        if era == "early":
            # Open top railings
            d.line([(bl + 1, bt + 3), (bl + 1, deck_div)],
                   fill=DARK_GREY, width=1)
            d.line([(br - 1, bt + 3), (br - 1, deck_div)],
                   fill=DARK_GREY, width=1)
            d.line([(bl + 1, bt + 3), (br - 1, bt + 3)],
                   fill=MED_GREY, width=1)
        else:
            # Upper rear window
            d.rectangle([bl + 4, bt + 3, br - 4, deck_div - 2],
                        fill=GLASS, outline=FRAME)

        # Lower rear window
        rw_top = deck_div + 3
        rw_bot = bb - 4
    else:
        rw_top = bt + 4
        rw_bot = bt + (bb - bt) // 2 - 1

    d.rectangle([bl + 4, rw_top, br - 4, rw_bot],
                fill=GLASS, outline=FRAME)

    # Tail lights
    d.rectangle([bl + 1, bb - 4, bl + 3, bb - 2], fill=RED_LIGHT)
    d.rectangle([br - 3, bb - 4, br - 1, bb - 2], fill=RED_LIGHT)

    # Destination board (rear)
    if era != "futuristic":
        db_y = bt - 2 if bt - 2 >= oy else bt
        d.rectangle([bl + 4, db_y, br - 4, db_y + 3], fill=s.trim)


# ── S (front / heading toward camera) view ───────────────────────────

def _draw_south(img: Image.Image, s: BusStyle, ox: int, oy: int,
                w: int, h: int):
    d = ImageDraw.Draw(img)
    era = s.era
    wr, wstyle = _wheel_params(era)

    shadow_h = 5
    gy = oy + h - shadow_h
    d.rectangle([ox + 4, gy, ox + w - 4, oy + h - 1], fill=SHADOW)

    _draw_wheel(d, ox + 6, gy - wr + 2, min(wr, 5), wstyle)
    _draw_wheel(d, ox + w - 6, gy - wr + 2, min(wr, 5), wstyle)

    ch = 3
    ch_y = gy - wr - ch + 2
    d.rectangle([ox + 3, ch_y, ox + w - 3, ch_y + ch], fill=s.chassis_color)

    bl = ox + 2
    br = ox + w - 2
    bb = ch_y
    bt = oy + (8 if s.double_deck else int(h * 0.30))

    if era == "futuristic":
        d.rounded_rectangle([bl, bt, br, bb], radius=4, fill=s.primary)
    else:
        d.rectangle([bl, bt, br, bb], fill=s.primary)

    d.line([(bl, bt), (br, bt)], fill=s.trim, width=1)

    if s.double_deck:
        deck_div = bt + (bb - bt) // 2 + 2
        d.rectangle([bl, bt, br, deck_div], fill=s.lighter)
        d.line([(bl, deck_div), (br, deck_div)], fill=s.trim, width=1)

        if era == "early":
            d.line([(bl + 1, bt + 3), (bl + 1, deck_div)],
                   fill=DARK_GREY, width=1)
            d.line([(br - 1, bt + 3), (br - 1, deck_div)],
                   fill=DARK_GREY, width=1)
            d.line([(bl + 1, bt + 3), (br - 1, bt + 3)],
                   fill=MED_GREY, width=1)
        else:
            d.rectangle([bl + 3, bt + 3, br - 3, deck_div - 2],
                        fill=GLASS, outline=FRAME)

        fw_top = deck_div + 3
        fw_bot = bb - 4
    else:
        fw_top = bt + 3
        fw_bot = bt + (bb - bt) // 2

    # Front windshield (larger than rear)
    if era in ("modern", "contemporary", "futuristic"):
        d.rectangle([bl + 2, fw_top, br - 2, fw_bot + 2],
                    fill=GLASS, outline=FRAME)
    else:
        d.rectangle([bl + 4, fw_top, br - 4, fw_bot],
                    fill=GLASS, outline=FRAME)

    # Headlights
    d.ellipse([bl, bb - 5, bl + 4, bb - 1], fill=GOLD, outline=DARK_GREY)
    d.ellipse([br - 4, bb - 5, br, bb - 1], fill=GOLD, outline=DARK_GREY)

    # Front destination board
    if era != "futuristic":
        db_y = bt - 2 if bt - 2 >= oy else bt
        d.rectangle([bl + 3, db_y, br - 3, db_y + 3], fill=s.trim)

    # Bumper (modern+)
    if era in ("modern", "contemporary", "futuristic"):
        d.rectangle([bl + 2, bb - 1, br - 2, bb], fill=MED_GREY)


# ── Diagonal views ────────────────────────────────────────────────────
# NE: heading NE, camera sees south side + rear face
# SW: heading SW, camera sees north side + front face
# SE = mirror of NE, NW = mirror of SW

def _draw_ne(img: Image.Image, s: BusStyle, ox: int, oy: int,
             w: int, h: int):
    """NE view: 3/4 showing side + rear via sheared parallelogram."""
    d = ImageDraw.Draw(img)
    era = s.era
    wr, wstyle = _wheel_params(era)

    shadow_h = 6
    gy = oy + h - shadow_h
    d.polygon([(ox + 15, gy), (ox + w - 10, gy),
               (ox + w - 5, gy + 5), (ox + 10, gy + 5)], fill=SHADOW)

    # Wheels
    _draw_wheel(d, ox + 18, gy - wr + 2, min(wr, 6), wstyle)
    _draw_wheel(d, ox + w - 22, gy - wr - 2, min(wr, 6), wstyle)

    # Body as sheared parallelogram
    shear = 12
    bb = gy - wr - 4
    bt = oy + (10 if s.double_deck else int(h * 0.30))
    bl = ox + 8
    br = ox + w - 8

    body = [(bl + shear, bt), (br, bt), (br - shear, bb), (bl, bb)]

    if era == "futuristic":
        # Approximate rounded with polygon
        d.polygon(body, fill=s.primary, outline=s.secondary)
    else:
        d.polygon(body, fill=s.primary)

    # Top trim
    d.line([(bl + shear, bt), (br, bt)], fill=s.trim, width=1)
    d.line([(bl + shear, bt + 1), (br, bt + 1)], fill=s.trim, width=1)
    d.line([(bl, bb), (br - shear, bb)], fill=s.secondary, width=1)

    # Waistline (early/classic)
    if era in ("early", "classic"):
        wm = (bt + bb) // 2
        d.line([(bl + shear // 2, wm), (br - shear // 2, wm)],
               fill=s.trim, width=1)

    # Double-deck
    if s.double_deck:
        dd = bt + (bb - bt) // 2 + 1
        upper = [(bl + shear, bt), (br, bt),
                 (br - shear // 2, dd), (bl + shear // 2, dd)]
        d.polygon(upper, fill=s.lighter)
        d.line([(bl + shear // 2, dd), (br - shear // 2, dd)],
               fill=s.trim, width=1)

        if era == "early":
            for i in range(4):
                px = bl + shear + 4 + i * 14
                if px > br - 10: break
                d.line([(px, bt + 4), (px - 2, dd)],
                       fill=DARK_GREY, width=1)
            d.line([(bl + shear + 4, bt + 3), (br - 6, bt + 3)],
                   fill=MED_GREY, width=1)
        else:
            # Upper windows
            win_w, gap = _window_params(era)
            wt = bt + 4
            wb = dd - 3
            for i in range(5):
                wx = bl + shear + 6 + i * (win_w + gap)
                if wx + win_w > br - 8: break
                pts = [(wx + 1, wt), (wx + win_w + 1, wt),
                       (wx + win_w - 1, wb), (wx - 1, wb)]
                d.polygon(pts, fill=GLASS)

        win_top = dd + 3
        win_bot = bb - 3
    else:
        if era in ("early", "classic"):
            win_top = bt + 4
            win_bot = (bt + bb) // 2 - 1
        else:
            win_top = bt + 3
            win_bot = bb - 4

    # Side windows
    win_w, gap = _window_params(era)
    for i in range(5):
        wx = bl + shear + 6 + i * (win_w + gap)
        if wx + win_w > br - 8: break
        pts = [(wx + 1, win_top), (wx + win_w + 1, win_top),
               (wx + win_w - 1, win_bot), (wx - 1, win_bot)]
        d.polygon(pts, fill=GLASS)
        if era in ("early", "classic"):
            d.polygon(pts, outline=FRAME)

    # Rear face (left edge)
    rear = [(bl + shear, bt), (bl, bb), (bl + 2, bb), (bl + shear + 2, bt)]
    d.polygon(rear, fill=s.darker)

    # Rear tail light
    d.rectangle([bl + 1, bb - 5, bl + 3, bb - 3], fill=RED_LIGHT)

    # Headlamp at front
    d.ellipse([br - shear - 4, bb - 6, br - shear, bb - 2],
              fill=GOLD, outline=DARK_GREY)

    # Destination board
    if era != "futuristic":
        d.rectangle([br - 16, bt - 2, br - 4, bt], fill=s.trim)


def _draw_se(img: Image.Image, s: BusStyle, ox: int, oy: int,
             w: int, h: int):
    temp = Image.new("RGBA", (w, h), TRANSPARENT)
    _draw_ne(temp, s, 0, 0, w, h)
    temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(temp, (ox, oy), temp)


def _draw_sw(img: Image.Image, s: BusStyle, ox: int, oy: int,
             w: int, h: int):
    """SW view: 3/4 showing side + front."""
    d = ImageDraw.Draw(img)
    era = s.era
    wr, wstyle = _wheel_params(era)

    shadow_h = 6
    gy = oy + h - shadow_h
    d.polygon([(ox + 10, gy), (ox + w - 15, gy),
               (ox + w - 10, gy + 5), (ox + 5, gy + 5)], fill=SHADOW)

    _draw_wheel(d, ox + w - 18, gy - wr + 2, min(wr, 6), wstyle)
    _draw_wheel(d, ox + 22, gy - wr - 2, min(wr, 6), wstyle)

    shear = 12
    bb = gy - wr - 4
    bt = oy + (10 if s.double_deck else int(h * 0.30))
    bl = ox + 8
    br = ox + w - 8

    body = [(bl, bt), (br - shear, bt), (br, bb), (bl + shear, bb)]
    if era == "futuristic":
        d.polygon(body, fill=s.primary, outline=s.secondary)
    else:
        d.polygon(body, fill=s.primary)

    d.line([(bl, bt), (br - shear, bt)], fill=s.trim, width=1)
    d.line([(bl, bt + 1), (br - shear, bt + 1)], fill=s.trim, width=1)
    d.line([(bl + shear, bb), (br, bb)], fill=s.secondary, width=1)

    if era in ("early", "classic"):
        wm = (bt + bb) // 2
        d.line([(bl + shear // 2, wm), (br - shear // 2, wm)],
               fill=s.trim, width=1)

    if s.double_deck:
        dd = bt + (bb - bt) // 2 + 1
        upper = [(bl, bt), (br - shear, bt),
                 (br - shear // 2, dd), (bl + shear // 2, dd)]
        d.polygon(upper, fill=s.lighter)
        d.line([(bl + shear // 2, dd), (br - shear // 2, dd)],
               fill=s.trim, width=1)

        if era == "early":
            for i in range(4):
                px = bl + 6 + i * 14
                if px > br - shear - 8: break
                d.line([(px, bt + 4), (px + 2, dd)],
                       fill=DARK_GREY, width=1)
            d.line([(bl + 6, bt + 3), (br - shear - 4, bt + 3)],
                   fill=MED_GREY, width=1)
        else:
            win_w, gap = _window_params(era)
            wt = bt + 4
            wb = dd - 3
            for i in range(5):
                wx = bl + 6 + i * (win_w + gap)
                if wx + win_w > br - shear - 6: break
                pts = [(wx - 1, wt), (wx + win_w - 1, wt),
                       (wx + win_w + 1, wb), (wx + 1, wb)]
                d.polygon(pts, fill=GLASS)

        win_top = dd + 3
        win_bot = bb - 3
    else:
        if era in ("early", "classic"):
            win_top = bt + 4
            win_bot = (bt + bb) // 2 - 1
        else:
            win_top = bt + 3
            win_bot = bb - 4

    win_w, gap = _window_params(era)
    for i in range(5):
        wx = bl + 6 + i * (win_w + gap)
        if wx + win_w > br - shear - 6: break
        pts = [(wx - 1, win_top), (wx + win_w - 1, win_top),
               (wx + win_w + 1, win_bot), (wx + 1, win_bot)]
        d.polygon(pts, fill=GLASS)
        if era in ("early", "classic"):
            d.polygon(pts, outline=FRAME)

    # Front face (right edge)
    front = [(br - shear, bt), (br, bb), (br - 2, bb), (br - shear - 2, bt)]
    d.polygon(front, fill=s.darker)

    # Headlamp on front face
    d.ellipse([br - 3, bb - 6, br + 1, bb - 2], fill=GOLD, outline=DARK_GREY)

    # Tail light on rear
    d.rectangle([bl + shear + 1, bb - 5, bl + shear + 3, bb - 3],
                fill=RED_LIGHT)

    if era != "futuristic":
        d.rectangle([bl + 4, bt - 2, bl + 16, bt], fill=s.trim)


def _draw_nw(img: Image.Image, s: BusStyle, ox: int, oy: int,
             w: int, h: int):
    temp = Image.new("RGBA", (w, h), TRANSPARENT)
    _draw_sw(temp, s, 0, 0, w, h)
    temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(temp, (ox, oy), temp)


# ── View dispatch ─────────────────────────────────────────────────────

_VIEW_FUNCS = {
    "N":  _draw_north,
    "NE": _draw_ne,
    "E":  _draw_east,
    "SE": _draw_se,
    "S":  _draw_south,
    "SW": _draw_sw,
    "W":  _draw_west,
    "NW": _draw_nw,
}


# ── Main entry point ─────────────────────────────────────────────────

def generate_bus_sprites(style: BusStyle, output_dir: Path):
    """Generate 4x and 1x 32bpp sprite sheets for a bus."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sheet_4x = Image.new("RGBA", (SHEET_W_4X, SHEET_H_4X), TRANSPARENT)
    for name, vx, vy, vw, vh in VIEWS_4X:
        _VIEW_FUNCS[name](sheet_4x, style, vx, vy, vw, vh)

    path_4x = output_dir / f"{style.slug}_4x.png"
    sheet_4x.save(path_4x, "PNG")

    sheet_1x = sheet_4x.resize(
        (SHEET_W_4X // 4, SHEET_H_4X // 4), Image.LANCZOS)
    path_1x = output_dir / f"{style.slug}_1x.png"
    sheet_1x.save(path_1x, "PNG")

    print(f"  {style.slug}: {path_4x.name} + {path_1x.name}")
    return path_4x, path_1x

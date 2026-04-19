#!/usr/bin/env python3
"""Generate 8bpp TTD-palette fallback sprites from 32bpp RGBA source.

Uses the exact DOS palette extracted from nmlc (nml.palette.palette_data[0]).
The palette binary is stored at sprites/tools/ttd_dos_palette.bin.
"""

from pathlib import Path
from PIL import Image

PALETTE_BIN = Path(__file__).parent / "ttd_dos_palette.bin"

def load_palette():
    """Load the 768-byte DOS palette from the binary file."""
    return PALETTE_BIN.read_bytes()

DOS_PAL = load_palette()

# Build lookup: RGB -> nearest palette index (skip index 0 = transparent)
_palette_rgb = []
for i in range(256):
    _palette_rgb.append((DOS_PAL[i*3], DOS_PAL[i*3+1], DOS_PAL[i*3+2]))

def nearest_index(r, g, b):
    best_i = 1
    best_d = 999999
    for i in range(1, 256):
        pr, pg, pb = _palette_rgb[i]
        if pr == 0 and pg == 0 and pb == 0 and i > 16:
            continue  # skip unused zero entries
        d = (r - pr)**2 + (g - pg)**2 + (b - pb)**2
        if d < best_d:
            best_d = d
            best_i = i
    return best_i


def convert(src_path, dst_path):
    rgba = Image.open(src_path).convert("RGBA")
    w, h = rgba.size
    pal_img = Image.new("P", (w, h), 0)
    pal_img.putpalette(DOS_PAL)

    src_px = rgba.load()
    dst_px = pal_img.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = src_px[x, y]
            if a > 128:
                dst_px[x, y] = nearest_index(r, g, b)
            # else stays 0 (transparent)

    pal_img.save(dst_path)
    print(f"  {dst_path} ({w}x{h})")


def batch_convert(root_dir: Path, pattern: str = "*_1x.png"):
    """Convert all matching 32bpp PNGs under root_dir to 8bpp."""
    sources = sorted(root_dir.rglob(pattern))
    # Also find 4x versions
    sources += sorted(root_dir.rglob(pattern.replace("_1x.", "_4x.")))
    # Deduplicate and skip already-converted files
    seen = set()
    to_convert = []
    for src in sources:
        if "_8bpp" in src.name or src in seen:
            continue
        seen.add(src)
        dst = src.with_name(src.stem + "_8bpp.png")
        to_convert.append((src, dst))
    return to_convert


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert 32bpp sprites to 8bpp TTD palette")
    parser.add_argument("--dir", "-d", type=Path, default=None,
                        help="Directory to scan (default: sprites/ tree)")
    parser.add_argument("--file", "-f", type=Path, default=None,
                        help="Convert a single file")
    args = parser.parse_args()

    if args.file:
        dst = args.file.with_name(args.file.stem + "_8bpp.png")
        print("Converting to 8bpp TTD palette:")
        convert(args.file, dst)
    else:
        root = args.dir or Path(__file__).parent.parent
        pairs = batch_convert(root)
        if not pairs:
            print("No files to convert.")
        else:
            print(f"Converting {len(pairs)} files to 8bpp TTD palette:")
            for src, dst in pairs:
                convert(src, dst)
    print("Done!")

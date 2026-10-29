#!/usr/bin/env python3
"""Encode browser-rendered Atlas frames as looping README GIFs (requires Pillow)."""
import argparse
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('frames', type=Path, help='Directory containing dark-000.png through light-095.png')
args = parser.parse_args()
assets = Path(__file__).resolve().parents[2] / 'assets'
for theme in ('dark', 'light'):
    frames = [Image.open(args.frames / f'{theme}-{i:03}.png').convert('RGB') for i in range(96)]
    if any(frame.size != (840, 320) for frame in frames):
        raise ValueError('Every captured frame must be 840 × 320 pixels')
    for index, frame in enumerate(frames):
        low, high = frame.crop((590, 60, 780, 260)).getextrema()[0]
        if high - low < 100:
            raise ValueError(f'Missing Atlas globe in {theme} frame {index}')
    # One shared palette avoids color flicker in the static header text.
    strip = Image.new('RGB', (840, 320 * 8))
    for j, i in enumerate(range(0, 96, 12)):
        strip.paste(frames[i], (0, j * 320))
    palette = strip.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    encoded = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    name = 'header-atlas' + ('-light' if theme == 'light' else '')
    encoded[0].save(assets / f'{name}.gif', save_all=True, append_images=encoded[1:],
                    duration=120, loop=0, optimize=True, disposal=1)
    frames[0].save(assets / f'{name}.png')
    print(f'{name}.gif: {(assets / (name + ".gif")).stat().st_size:,} bytes')

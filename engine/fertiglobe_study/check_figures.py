"""Programmatic readability check on every figure figures.py produces.

Fails loudly — non-zero exit and an AssertionError-style report — if any figure is
not a fully opaque, light-canvas PNG at the expected pixel size. Run it after
figures.py, every time; a figure that fails this check must not go into a document.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

DPI = 300
W = 6.5  # inches — must match figures.py

# name -> (width_inches, height_inches) as passed to plt.subplots(figsize=...)
EXPECTED = {
    'fig1_football.png': (W, 4.7),
    'fig2_sens.png': (W, 4.3),
    'fig3_costpass.png': (W, 4.35),
    'fig4_fan.png': (W, 3.9),
    'fig5_dist.png': (W, 3.8),
    'fig6_segments.png': (W, 5.5),
    'fig7_waterfall.png': (W, 4.6),
    'figD1_experts.png': (W, 3.6),
}

MIN_MEAN_LUMINANCE = 0.80   # a light canvas; a dark background scores far below this
MIN_CORNER_LUMINANCE = 0.85  # the page margins themselves must be light
MIN_INK_CONTRAST = 0.35      # darkest text must stand well clear of the background


def luminance(rgb):
    """Rec. 709 relative luminance, rgb in 0..1."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def check(name, size_in):
    path = os.path.join(HERE, name)
    problems = []
    if not os.path.exists(path):
        return [f'{name}: MISSING — figures.py did not produce it']

    im = Image.open(path)
    exp = (int(round(size_in[0] * DPI)), int(round(size_in[1] * DPI)))
    if im.size != exp:
        problems.append(f'{name}: size {im.size} != expected {exp}')

    rgba = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    alpha = rgba[..., 3]
    if alpha.min() < 1.0:
        n = int((alpha < 1.0).sum())
        problems.append(f'{name}: NOT OPAQUE — {n} pixels with alpha < 255 '
                        f'(min alpha {alpha.min() * 255:.0f})')

    lum = luminance(rgba[..., :3])
    mean_lum = float(lum.mean())
    if mean_lum < MIN_MEAN_LUMINANCE:
        problems.append(f'{name}: background too dark — mean luminance {mean_lum:.3f} '
                        f'< {MIN_MEAN_LUMINANCE}')

    h, w = lum.shape
    k = max(4, min(h, w) // 100)
    corners = np.array([lum[:k, :k].mean(), lum[:k, -k:].mean(),
                        lum[-k:, :k].mean(), lum[-k:, -k:].mean()])
    if corners.min() < MIN_CORNER_LUMINANCE:
        problems.append(f'{name}: canvas corner is not light — darkest corner '
                        f'{corners.min():.3f} < {MIN_CORNER_LUMINANCE}')

    # something must actually be drawn, and it must contrast with the canvas
    contrast = float(np.percentile(lum, 99.5) - np.percentile(lum, 0.2))
    if contrast < MIN_INK_CONTRAST:
        problems.append(f'{name}: too little contrast between ink and canvas '
                        f'({contrast:.3f} < {MIN_INK_CONTRAST})')

    if not problems:
        print(f'  PASS  {name:24s} {im.size[0]}x{im.size[1]}px  opaque  '
              f'mean luminance {mean_lum:.3f}  contrast {contrast:.3f}')
    return problems


def main():
    print('checking figures in', HERE)
    failures = []
    for name, size_in in EXPECTED.items():
        failures.extend(check(name, size_in))
    stray = [f for f in sorted(os.listdir(HERE))
             if f.lower().endswith('.png') and f not in EXPECTED]
    if stray:
        failures.append(f'unexpected PNG(s) present, not covered by this check: {stray}')
    if failures:
        print('\nFIGURE CHECK FAILED')
        for f in failures:
            print('  *', f)
        sys.exit(1)
    print(f'\nall {len(EXPECTED)} figures pass: fully opaque, light canvas, '
          f'expected pixel dimensions')


if __name__ == '__main__':
    main()

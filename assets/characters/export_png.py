# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Export every SVG in svg/on-dark and svg/on-light to a 512 x 512 transparent PNG in png/.
Uses headless Chrome, Chromium or Edge (tools/headless.py finds it; set CHROME to override)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
from headless import svg_to_png  # noqa: E402
if len(sys.argv) > 1 and sys.argv[1] == 'v2':
    HERE = os.path.join(HERE, 'v2')  # uv run export_png.py v2
SIZE = 512

for sub in ('on-dark', 'on-light'):
    src, dst = os.path.join(HERE, 'svg', sub), os.path.join(HERE, 'png', sub)
    os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(src)):
        if not name.endswith('.svg'):
            continue
        svg = open(os.path.join(src, name)).read().replace('<svg ', f'<svg width="{SIZE}" height="{SIZE}" ', 1)
        svg_to_png(svg, os.path.join(dst, name[:-4] + '.png'), SIZE, SIZE)
    print(sub, len(os.listdir(dst)), 'png')

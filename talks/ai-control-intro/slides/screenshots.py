# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Screenshot slides at 1920x1080 with headless Chrome, Chromium or Edge (any OS).

usage: uv run screenshots.py en|es [N ...]   -> screenshots/<lang>-NN.png, every slide or only slides N

Writes the preview page first (preview.py), then shoots its ?solo=N view of each slide.
Set CHROME to a browser binary if none is found.
"""
import json
import os
import sys

from preview import HERE, main as write_preview

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from headless import file_url, screenshot  # noqa: E402


def shoot(lang, numbers):
    write_preview(lang)
    page = file_url(os.path.join(HERE, f'preview-{lang}.html'))
    total = len(json.load(open(os.path.join(HERE, lang, 'project', 'deck.json'), encoding='utf-8'))['order'])
    out = os.path.join(HERE, 'screenshots')
    os.makedirs(out, exist_ok=True)
    for n in numbers or range(1, total + 1):
        png = os.path.join(out, f'{lang}-{n:02d}.png')
        screenshot(f'{page}?solo={n}', png, 1920, 1080, wait_ms=6000)
        print(png)


if __name__ == '__main__':
    shoot(sys.argv[1] if len(sys.argv) > 1 else 'en', [int(n) for n in sys.argv[2:]])

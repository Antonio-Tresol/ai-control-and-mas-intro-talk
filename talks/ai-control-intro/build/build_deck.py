# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Write every slide of the deck to out/project/slides/<id>.html in one look.

Usage: uv run build_deck.py [dark|light] [sketch|clean] [module ...]
Defaults: dark sketch, all act modules. Then: uv run preview.py
Each act module defines SLIDES = [(slide_id, function), ...]; each function takes the token
set T and returns one <section> string (gen.SECTION) whose id equals slide_id.
"""
import importlib
import json
import os
import sys

import glyphs
import gen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'project', 'slides')
MODULES = ['act1', 'act2', 'act34']


def main(argv):
    theme = 'light' if 'light' in argv else 'dark'
    glyphs.SKETCH_DEFAULT = 'clean' not in argv
    mods = [a for a in argv if a in MODULES] or MODULES
    T = glyphs.LIGHT if theme == 'light' else glyphs.DARK
    gen.DARK = T  # specimen helpers that read DARK follow the chosen look
    os.makedirs(OUT, exist_ok=True)
    order = json.load(open(os.path.join(HERE, 'order.json')))
    written = []
    for name in mods:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            print('skip (not written yet):', name)
            continue
        for sid, fn in mod.SLIDES:
            assert sid in order, f'{sid} is not in order.json'
            glyphs.begin_slide(sid)
            html = fn(T)
            assert f'<section id="{sid}"' in html, f'{sid}: section id must equal the slide id'
            open(os.path.join(OUT, f'{sid}.html'), 'w', encoding='utf-8').write(html)
            written.append(sid)
    print(theme, 'sketch' if glyphs.SKETCH_DEFAULT else 'clean', 'wrote', len(written), 'slides:', ' '.join(written))


if __name__ == '__main__':
    main(sys.argv[1:])

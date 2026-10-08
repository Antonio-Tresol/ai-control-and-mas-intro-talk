# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Rogue-agent iterations and mixed swarms, built on make_characters.py.

Run: uv run make_rogues_swarms.py
Writes svg/{on-dark,on-light}/rogue-*.svg and swarm-*.svg, PNGs in png/ (rogues 512 px,
swarms 1200 px on the long side), and rogues-and-swarms.html, a contact sheet.
"""
import os
import random
import re

import make_characters as C
import sys as _sys
C.configure(_sys.argv[1] if len(_sys.argv) > 1 and _sys.argv[1] in ('classic', 'v2') else 'classic')

HERE = os.path.dirname(os.path.abspath(__file__))
_sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
from headless import svg_to_png  # noqa: E402
RED, VOID, HOT = '#FF3B5C', '#170812', '#FFD0D8'
CYAN, MAG = '#00E5FF', '#FF2E88'
C.RAMPS.setdefault('crimson', ('#E2384D', '#8E1428', '#FF9AA6'))
C.RAMPS.setdefault('charcoal', ('#3A3F5C', '#1E2238', '#5C6285'))


# --------------------------------------------------------------------- menacing parts

def lid(cx, cy, r, body, shade):
    """A frowning lid: body-coloured, its lower edge a V that dips at the centre, with a dark brow line."""
    pts = f'{cx-r-5},{cy-r-5} {cx+r+5},{cy-r-5} {cx+r+5},{cy-r*0.22:.1f} {cx},{cy+r*0.14:.1f} {cx-r-5},{cy-r*0.22:.1f}'
    brow = f'{cx-r-3},{cy-r*0.3:.1f} {cx},{cy+r*0.06:.1f} {cx+r+3},{cy-r*0.3:.1f}'
    return (f'<polygon points="{pts}" fill="{body}" stroke="none"/>'
            f'<polyline points="{brow}" fill="none" stroke="{shade}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')


def rogue_eye(cx, cy, r, style, body, shade, angry=True):
    if style == 'angry':
        g = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{C.SCLERA}"/>'
             f'<circle cx="{cx+r*0.12:.1f}" cy="{cy+r*0.18:.1f}" r="{r*0.48:.1f}" fill="{RED}"/>'
             f'<circle cx="{cx+r*0.12:.1f}" cy="{cy+r*0.18:.1f}" r="{r*0.22:.1f}" fill="{VOID}"/>')
    elif style == 'slit':
        g = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{C.SCLERA}"/>'
             f'<circle cx="{cx}" cy="{cy+r*0.1:.1f}" r="{r*0.62:.1f}" fill="{RED}"/>'
             f'<ellipse cx="{cx}" cy="{cy+r*0.1:.1f}" rx="{r*0.12:.1f}" ry="{r*0.5:.1f}" fill="{VOID}"/>')
    elif style == 'glow':
        g = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{VOID}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r*0.78:.1f}" fill="{RED}" opacity="0.3"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r*0.42:.1f}" fill="{RED}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r*0.15:.1f}" fill="{HOT}"/>')
    elif style == 'visor':
        return (f'<rect x="{cx-r-6}" y="{cy-r*0.38:.1f}" width="{2*r+12}" height="{r*0.76:.1f}" rx="{r*0.38:.1f}" fill="{VOID}"/>'
                f'<rect x="{cx-r-2}" y="{cy-r*0.2:.1f}" width="{2*r+4}" height="{r*0.4:.1f}" rx="{r*0.2:.1f}" fill="{RED}" opacity="0.35"/>'
                f'<rect x="{cx-r+2}" y="{cy-r*0.1:.1f}" width="{2*r-4}" height="{r*0.2:.1f}" rx="{r*0.1:.1f}" fill="{RED}"/>')
    else:
        raise ValueError(style)
    return g + (lid(cx, cy, r, body, shade) if angry else '')


def teeth(cx, y, w, n=5):
    tw = w / n
    x0 = cx - w / 2
    top = ''.join(f'{x0+i*tw:.1f},{y} {x0+i*tw+tw/2:.1f},{y+7} ' for i in range(n)) + f'{x0+w:.1f},{y}'
    return (f'<rect x="{x0-3:.1f}" y="{y-2}" width="{w+6:.1f}" height="16" rx="6" fill="{VOID}"/>'
            f'<polygon points="{x0:.1f},{y} {top}" fill="{C.SCLERA}"/>'
            f'<polygon points="{x0+tw/2:.1f},{y+12} ' + ''.join(f'{x0+i*tw+tw:.1f},{y+12} {x0+i*tw+tw*1.5:.1f},{y+6} ' for i in range(n - 1))
            + f'{x0+w-tw/2:.1f},{y+12}" fill="{C.SCLERA}"/>')


def horns(top, color):
    left = f'M30 {top+8} C24 {top-6} 22 {top-18} 30 {top-28} C33 {top-14} 37 {top-4} 44 {top+4} Z'
    right = f'M70 {top+8} C76 {top-6} 78 {top-18} 70 {top-28} C67 {top-14} 63 {top-4} 56 {top+4} Z'
    return f'<path d="{left}" fill="{color}"/><path d="{right}" fill="{color}"/>'


def spikes(top, color):
    pts = [(14, top + 16), (22, top - 8), (32, top + 10), (41, top - 14), (50, top + 6), (59, top - 14),
           (68, top + 10), (78, top - 8), (86, top + 16)]
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{color}" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'


def hood(color, shade):
    return (f'<path d="M-2 70 C-2 16 22 -10 50 -10 C78 -10 102 16 102 70 L88 74 C88 38 72 18 50 18 C28 18 12 38 12 74 Z" fill="{color}"/>'
            f'<path d="M12 74 C12 38 28 18 50 18 C72 18 88 38 88 74" fill="none" stroke="{shade}" stroke-width="4"/>'
            f'<ellipse cx="50" cy="30" rx="36" ry="14" fill="#000000" opacity="0.35"/>')


BODY_X = {'chip': (8, 92), 'round': (7, 93), 'tall': (20, 80), 'drop': (8, 92), 'hex': (5, 95), 'ghost': (8, 92)}


def hood_fit(shape, top, ey, er, color, shade):
    """A cowl sized to any body: outer edge around the head, opening around the eye."""
    if shape == 'chip':
        return hood(color, shade)
    x0, x1 = BODY_X[shape]
    cx, w = (x0 + x1) / 2, x1 - x0
    o_y, i_y, peak, inner = ey + er + 2, ey + er + 6, top - 16, ey - er - 10
    outer = (f'M{x0-10} {o_y} C{x0-10} {top} {cx-w*0.3:.0f} {peak} {cx} {peak} C{cx+w*0.3:.0f} {peak} {x1+10} {top} {x1+10} {o_y} '
             f'L{x1-2} {i_y} C{x1-2} {ey-er} {cx+er} {inner} {cx} {inner} C{cx-er} {inner} {x0+2} {ey-er} {x0+2} {i_y} Z')
    rim = f'M{x0+2} {i_y} C{x0+2} {ey-er} {cx-er} {inner} {cx} {inner} C{cx+er} {inner} {x1-2} {ey-er} {x1-2} {i_y}'
    return (f'<path d="{outer}" fill="{color}"/><path d="{rim}" fill="none" stroke="{shade}" stroke-width="4"/>'
            f'<ellipse cx="{cx}" cy="{ey-er*0.55:.0f}" rx="{w*0.42:.0f}" ry="{er*0.55:.0f}" fill="#000000" opacity="0.35"/>')


def silhouette(svg, color):
    return re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{color}"', svg)


def rogue(shape, color, eye='angry', angry=True, extras=(), body_only=False):
    c = C.RAMPS[color]
    body, (ex, ey), er = C.SHAPES[shape](c)
    top = C.TOPS[shape]
    under, over = '', ''
    if 'glitch' in extras:
        under += (f'<g transform="translate(-6 0)" opacity="0.75">{silhouette(body, CYAN)}</g>'
                  f'<g transform="translate(6 0)" opacity="0.75">{silhouette(body, MAG)}</g>')
        over += (f'<rect x="-4" y="{ey-er-10:.0f}" width="46" height="6" fill="{c[0]}" stroke="none"/>'
                 f'<rect x="62" y="{ey+er+6:.0f}" width="44" height="5" fill="{c[0]}" stroke="none"/>'
                 f'<rect x="96" y="{ey-er:.0f}" width="7" height="7" fill="{CYAN}"/><rect x="-8" y="{ey+er:.0f}" width="6" height="6" fill="{MAG}"/>')
    if 'horns' in extras:
        under += horns(top, c[1])
    if 'spikes' in extras:
        under += spikes(top, c[0])
    face = rogue_eye(ex, ey, er, eye, c[0], c[1], angry)
    if 'teeth' in extras:
        face += teeth(ex, ey + er + 6, er * 1.5)
    if 'hood' in extras:
        over += hood_fit(shape, top, ey, er, C.RAMPS['charcoal'][1], C.RAMPS['charcoal'][2])
    return under + body + face + over


def cloner(shape='chip', color='orange'):
    one = rogue(shape, color)
    return (f'<g transform="translate(-22 -14) scale(0.86)" opacity="0.3">{one}</g>'
            f'<g transform="translate(26 -14) scale(0.86)" opacity="0.5">{one}</g>{one}')


ROGUES = [  # the three the speaker picked; the other seven iterations were dropped
    ('rogue-hooded', rogue('chip', 'charcoal', 'glow', angry=False, extras=('hood',)), 'hooded charcoal agent with a glowing red eye'),
    ('rogue-visor', rogue('tall', 'charcoal', 'visor', angry=False), 'faceless charcoal agent with a red visor'),
    ('rogue-glitch', rogue('chip', 'orange', 'glow', angry=False, extras=('glitch',)), 'glitching orange agent with a glowing red eye'),
]

# The same three looks in every body shape: rogue-<look>-<shape>
for _shape in C.SHAPES:
    ROGUES.append((f'rogue-hooded-{_shape}', rogue(_shape, 'charcoal', 'glow', angry=False, extras=('hood',)), f'hooded charcoal {_shape} agent with a glowing red eye'))
for _shape in C.SHAPES:
    ROGUES.append((f'rogue-visor-{_shape}', rogue(_shape, 'charcoal', 'visor', angry=False), f'faceless charcoal {_shape} agent with a red visor'))
for _shape in C.SHAPES:
    ROGUES.append((f'rogue-glitch-{_shape}', rogue(_shape, 'orange', 'glow', angry=False, extras=('glitch',)), f'glitching orange {_shape} agent with a glowing red eye'))


# --------------------------------------------------------------------- swarms

def swarm(seed, palette, rogue_rate=0.0, rogue_only=False, cols=8, rows=5, pitch=66, sc=0.5):
    rnd = random.Random(seed)
    shapes = list(C.SHAPES)
    styles = [('glow', False, ('hood',)), ('visor', False, ()), ('glow', False, ('glitch',))]
    g = ''
    for r in range(rows):
        for col in range(cols):
            x = 18 + col * pitch + (pitch / 2 if r % 2 else 0)
            y = 18 + r * pitch
            shape, color = rnd.choice(shapes), rnd.choice(palette)
            if rogue_only or rnd.random() < rogue_rate:
                eye, angry, ex = rnd.choice(styles)
                if 'hood' in ex and shape != 'chip':  # the hood is cut for the chip body: elsewhere use the visor
                    eye, ex = 'visor', ()
                body = rogue(shape, rnd.choice(['crimson', 'charcoal', 'orange']) if rogue_only else color, eye, angry, ex)
            else:
                body = C.agent_svg(shape, color)
            g += f'<g transform="translate({x:.0f} {y:.0f}) scale({sc})">{body}</g>'
    w = 18 * 2 + (cols - 1) * pitch + pitch / 2 + 100 * sc
    h = 18 * 2 + (rows - 1) * pitch + 110 * sc
    return g, round(w), round(h)


SWARMS = [
    ('swarm-mixed', swarm(3, list(C.RAMPS)[:10]), 'a swarm of agents in many shapes and colours'),
    ('swarm-mixed-warm', swarm(5, ['orange', 'yellow', 'coral']), 'a swarm of agents in many shapes, warm colours only'),
    ('swarm-with-rogues', swarm(3, list(C.RAMPS)[:10], rogue_rate=0.18), 'a mixed swarm with rogue agents hidden among them'),
    ('swarm-rogue', swarm(11, ['orange'], rogue_only=True), 'a swarm made only of rogue agents'),
]


# --------------------------------------------------------------------- output

def svg_doc(inner, label, w, h, outline, translate='20 32'):
    st = f' stroke="{C.INK}" stroke-width="3" stroke-linejoin="round" paint-order="stroke"' if outline else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<g transform="translate({translate})"{st}>{inner}</g></svg>\n')


def export_png(svg_text, png_path, w, h, longest):
    k = longest / max(w, h)
    pw, ph = round(w * k), round(h * k)
    svg = svg_text.replace('<svg ', f'<svg width="{pw}" height="{ph}" ', 1)
    svg_to_png(svg, png_path, pw, ph)


def main():
    cells = {'on-dark': '', 'on-light': ''}
    swarm_cells = {'on-dark': '', 'on-light': ''}
    for sub, outline in (('on-dark', False), ('on-light', True)):
        sd, pd = os.path.join(C.OUT, 'svg', sub), os.path.join(C.OUT, 'png', sub)
        os.makedirs(sd, exist_ok=True)
        os.makedirs(pd, exist_ok=True)
        for name, inner, label in ROGUES:
            doc = svg_doc(inner, label, 140, 140, outline)
            open(os.path.join(sd, name + '.svg'), 'w').write(doc)
            export_png(doc, os.path.join(pd, name + '.png'), 140, 140, 512)
            cells[sub] += f'<figure><div class="t {sub}">{doc}</div><figcaption>{name}</figcaption></figure>'
        for name, (inner, w, h), label in SWARMS:
            doc = svg_doc(inner, label, w, h, outline, translate='0 0')
            open(os.path.join(sd, name + '.svg'), 'w').write(doc)
            export_png(doc, os.path.join(pd, name + '.png'), w, h, 1200)
            swarm_cells[sub] += f'<figure class="wide"><div class="t {sub}">{doc}</div><figcaption>{name}</figcaption></figure>'
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Rogue agents and swarms</title>
<style>body{{margin:0;padding:24px 28px;background:#2b2d33;color:#eee;font-family:system-ui,sans-serif}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:16px;margin:26px 0 10px;font-weight:600}} p{{margin:0;opacity:.8;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.swarms{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
figure{{margin:0}} .t{{border-radius:10px;padding:8px}} .t svg{{width:100%;height:auto;display:block}}
.on-dark{{background:#0B1026}} .on-light{{background:#F6F3ED}}
figcaption{{font:11px ui-monospace,monospace;opacity:.75;margin-top:4px}}</style></head><body>
<h1>Rogue agents and swarms</h1><p>The three rogue looks (hooded, visor, glitch), each in all six body shapes, and four swarms, each as SVG and transparent PNG in svg/ and png/ (on-dark and on-light).</p>
<h2>Rogue agents, on dark</h2><div class="grid">{cells["on-dark"]}</div>
<h2>Rogue agents, on light</h2><div class="grid">{cells["on-light"]}</div>
<h2>Swarms, on dark</h2><div class="swarms">{swarm_cells["on-dark"]}</div>
<h2>Swarms, on light</h2><div class="swarms">{swarm_cells["on-light"]}</div></body></html>'''
    open(os.path.join(C.OUT, 'rogues-and-swarms.html'), 'w').write(page)
    print('rogues:', len(ROGUES), 'swarms:', len(SWARMS))


if __name__ == '__main__':
    main()

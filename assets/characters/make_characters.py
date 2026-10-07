"""Character asset pack: one-eyed agents in many colours and shapes, plus the small monitor robot.

Original designs (no traced or copied characters). Run:  python3 make_characters.py
Writes svg/on-dark/*.svg, svg/on-light/*.svg (same drawings with an ink outline for pale
backgrounds) and index.html, a contact sheet of everything. PNG exports: python3 export_png.py

Every drawing sits in a 140 x 140 viewBox with transparent background, so assets line up
when placed side by side. Colours come from RAMPS: body, shade (pins, feet, details), light
(highlight). Recolour an asset by swapping those three hex values.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SCLERA, IRIS, INK = '#FDFBFF', '#0B1026', '#1A2230'
YELLOW, PINK, GLASS, MINT = '#FFF251', '#DA86B4', '#0E2E4A', '#00996F'

# Two styles. 'classic': white eye with a dark iris, pink attack colour (the first set, kept for later use).
# 'v2' (chosen 2026-10-07): black eye with a white centre, red attack colour. v2 files go to v2/.
STYLE, INVERTED, OUT = 'classic', False, HERE


def configure(style):
    global STYLE, INVERTED, OUT, PINK
    assert style in ('classic', 'v2'), style
    STYLE, INVERTED = style, style == 'v2'
    PINK = '#FF3B5C' if INVERTED else '#DA86B4'
    OUT = os.path.join(HERE, 'v2') if INVERTED else HERE
GEAR = '#A3AADB'  # headset and other gear: light enough to read on navy

RAMPS = {
    'orange':   ('#F4AB1A', '#B87708', '#FFD98A'),
    'sky':      ('#A1D8FF', '#5D9BC9', '#F2FAFF'),
    'pink':     ('#F4A6C8', '#C2588A', '#FBD9E8'),
    'purple':   ('#9C8CF2', '#5E4FB8', '#D6CEFF'),
    'teal':     ('#3FD0B0', '#138A71', '#B8F2E4'),
    'green':    ('#8FD45A', '#4E8A1F', '#D6F2B8'),
    'coral':    ('#FF8A6B', '#C24A2C', '#FFD0C2'),
    'yellow':   ('#FFE45C', '#B89A0A', '#FFF4B0'),
    'lavender': ('#ECE8FF', '#A69EE0', '#FFFFFF'),
    'slate':    ('#A3AADB', '#6A72A8', '#D9DCF2'),
}

# --------------------------------------------------------------------- body shapes
# Each returns (svg for body + limbs, eye centre, eye radius). Canonical box 100 x 104,
# placed at (20, 32) inside the 140 x 140 viewBox.

def chip(c):
    b, sh, li = c
    g = ''.join(f'<rect x="{x}" y="{y}" width="12" height="9" rx="3" fill="{sh}"/>' for y in (34, 54) for x in (0, 88))
    g += f'<rect x="28" y="84" width="12" height="18" rx="5" fill="{sh}"/><rect x="60" y="84" width="12" height="18" rx="5" fill="{sh}"/>'
    g += f'<rect x="8" y="6" width="84" height="84" rx="28" fill="{b}"/><ellipse cx="30" cy="21" rx="11" ry="6" fill="{li}"/>'
    return g, (50, 48), 24


def round_(c):
    b, sh, li = c
    g = f'<rect x="30" y="84" width="12" height="18" rx="5" fill="{sh}"/><rect x="58" y="84" width="12" height="18" rx="5" fill="{sh}"/>'
    g += f'<circle cx="50" cy="50" r="43" fill="{b}"/><ellipse cx="30" cy="25" rx="11" ry="6" fill="{li}" transform="rotate(-30 30 25)"/>'
    return g, (50, 50), 23


def tall(c):
    b, sh, li = c
    g = f'<rect x="31" y="86" width="12" height="16" rx="5" fill="{sh}"/><rect x="57" y="86" width="12" height="16" rx="5" fill="{sh}"/>'
    g += f'<rect x="12" y="38" width="10" height="22" rx="5" fill="{sh}"/><rect x="78" y="38" width="10" height="22" rx="5" fill="{sh}"/>'
    g += f'<rect x="20" y="-4" width="60" height="94" rx="30" fill="{b}"/><ellipse cx="36" cy="10" rx="8" ry="5" fill="{li}"/>'
    return g, (50, 34), 20


def drop(c):
    b, sh, li = c
    g = f'<rect x="30" y="86" width="12" height="16" rx="5" fill="{sh}"/><rect x="58" y="86" width="12" height="16" rx="5" fill="{sh}"/>'
    g += (f'<path d="M50 -2 C62 18 92 40 92 62 C92 82 74 92 50 92 C26 92 8 82 8 62 C8 40 38 18 50 -2 Z" fill="{b}"/>'
          f'<ellipse cx="34" cy="44" rx="8" ry="5" fill="{li}" transform="rotate(-35 34 44)"/>')
    return g, (50, 60), 21


def hexa(c):
    b, sh, li = c
    g = f'<rect x="30" y="84" width="12" height="18" rx="5" fill="{sh}"/><rect x="58" y="84" width="12" height="18" rx="5" fill="{sh}"/>'
    g += (f'<path d="M50 2 L91 25 L91 71 L50 94 L9 71 L9 25 Z" fill="{b}" stroke="{b}" stroke-width="8" stroke-linejoin="round"/>'
          f'<path d="M24 26 L40 17" stroke="{li}" stroke-width="7" stroke-linecap="round"/>')
    return g, (50, 49), 23


def ghost(c):
    b, sh, li = c
    g = (f'<path d="M8 50 A42 42 0 0 1 92 50 V88 Q85 100 78 90 Q71 100 64 90 Q57 100 50 90 Q43 100 36 90 '
         f'Q29 100 22 90 Q15 100 8 88 Z" fill="{b}"/><ellipse cx="30" cy="24" rx="10" ry="5.5" fill="{li}" transform="rotate(-25 30 24)"/>')
    return g, (50, 48), 23


SHAPES = {'chip': chip, 'round': round_, 'tall': tall, 'drop': drop, 'hex': hexa, 'ghost': ghost}

# --------------------------------------------------------------------- accessories
# Drawn in canonical body coordinates; `c` is the body ramp, `top` the y of the head's top.

def acc_antenna(c, top):
    return (f'<line x1="50" y1="{top+2}" x2="50" y2="{top-16}" stroke="{c[1]}" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="50" cy="{top-19}" r="6" fill="{YELLOW}"/>')


def acc_cap(c, top):
    return (f'<path d="M26 {top+10} A24 16 0 0 1 74 {top+10} Z" fill="{c[1]}"/>'
            f'<rect x="58" y="{top+6}" width="30" height="7" rx="3.5" fill="{c[1]}"/>'
            f'<circle cx="50" cy="{top-5}" r="3.5" fill="{c[2]}"/>')


def acc_headset(c, top):
    return (f'<path d="M14 {top+34} A36 36 0 0 1 86 {top+34}" fill="none" stroke="{GEAR}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="4" y="{top+30}" width="14" height="24" rx="6" fill="{GEAR}"/><rect x="82" y="{top+30}" width="14" height="24" rx="6" fill="{GEAR}"/>')


def acc_sprout(c, top):
    return (f'<path d="M50 {top+3} C50 {top-8} 44 {top-14} 36 {top-14} C38 {top-6} 43 {top-1} 50 {top+3} Z" fill="{MINT}"/>'
            f'<path d="M50 {top+3} C51 {top-9} 58 {top-16} 66 {top-15} C63 {top-7} 57 {top-1} 50 {top+3} Z" fill="{MINT}"/>')


def acc_crown(c, top):
    return f'<path d="M30 {top+6} L32 {top-14} L42 {top-4} L50 {top-18} L58 {top-4} L68 {top-14} L70 {top+6} Z" fill="{YELLOW}"/>'


def acc_megaphone(c, top):
    return f'<path d="M90 56 L110 44 L110 78 L90 66 Z" fill="#ECE8FF"/><rect x="84" y="54" width="9" height="14" rx="3" fill="#ECE8FF"/>'


def acc_badge(c, top):
    return f'<path d="M84 {top-12} L100 {top+4} L84 {top+20} L68 {top+4} Z" fill="{PINK}" stroke="{IRIS}" stroke-width="4" stroke-linejoin="round"/>'


ACCESSORIES = {'antenna': acc_antenna, 'cap': acc_cap, 'headset': acc_headset, 'sprout': acc_sprout,
               'crown': acc_crown, 'megaphone': acc_megaphone, 'attack-badge': acc_badge}
TOPS = {'chip': 6, 'round': 7, 'tall': -4, 'drop': -2, 'hex': 2, 'ghost': 8}


def eye(cx, cy, r, look=(0.35, 0.1), iris=IRIS):
    if INVERTED:  # black eye, white centre (a coloured centre, e.g. the attack red, when one is passed)
        inner = SCLERA if iris == IRIS else iris
        return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{IRIS}"/>'
                f'<circle cx="{cx + look[0]*r*0.38:.1f}" cy="{cy + look[1]*r*0.38:.1f}" r="{r*0.5:.1f}" fill="{inner}"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SCLERA}"/>'
            f'<circle cx="{cx + look[0]*r*0.38:.1f}" cy="{cy + look[1]*r*0.38:.1f}" r="{r*0.5:.1f}" fill="{iris}"/>'
            f'<circle cx="{cx + r*0.3:.1f}" cy="{cy - r*0.2:.1f}" r="{r*0.17:.1f}" fill="{SCLERA}"/>')


def agent_svg(shape, color, accessory=None, iris=IRIS):
    c = RAMPS[color]
    body, (ex, ey), er = SHAPES[shape](c)
    top = TOPS[shape]
    behind = acc_headset(c, top) if accessory == 'headset' else ''
    front = ACCESSORIES[accessory](c, top) if accessory and accessory != 'headset' else ''
    if accessory == 'headset':
        front = (f'<rect x="4" y="{top+30}" width="14" height="24" rx="6" fill="{GEAR}"/>'
                 f'<rect x="82" y="{top+30}" width="14" height="24" rx="6" fill="{GEAR}"/>')
    inner = behind + body + eye(ex, ey, er, iris=iris) + front
    return inner


# --------------------------------------------------------------------- the monitor robot
# A small, sturdy robot: smaller than an agent (a weaker model), a visor for scanning.

def robot_svg(color='sky', mode='idle'):
    b, sh, li = RAMPS[color]
    scan = PINK if mode == 'alert' else b
    lamp = PINK if mode == 'alert' else YELLOW
    g = ''
    if mode == 'scanning':
        g += f'<path d="M86 52 L118 36 L118 80 Z" fill="{b}" opacity="0.28"/>'
    g += (f'<line x1="50" y1="20" x2="50" y2="8" stroke="{sh}" stroke-width="4" stroke-linecap="round"/>'
          f'<circle cx="50" cy="6" r="6" fill="{lamp}"/>'
          f'<rect x="4" y="46" width="10" height="18" rx="4" fill="{sh}"/><rect x="86" y="46" width="10" height="18" rx="4" fill="{sh}"/>'
          f'<rect x="28" y="88" width="14" height="14" rx="5" fill="{sh}"/><rect x="58" y="88" width="14" height="14" rx="5" fill="{sh}"/>'
          f'<rect x="10" y="20" width="80" height="72" rx="22" fill="{b}"/>'
          f'<ellipse cx="28" cy="31" rx="9" ry="5" fill="{li}"/>'
          f'<rect x="20" y="40" width="60" height="24" rx="12" fill="{GLASS}"/>'
          f'<rect x="{30 if mode != "alert" else 26}" y="49" width="{26 if mode != "alert" else 48}" height="6" rx="3" fill="{scan}"/>'
          f'<rect x="38" y="72" width="24" height="8" rx="4" fill="{sh}"/>')
    return g


def robot_absent_svg():
    d = 'stroke="#8A93C9" stroke-width="4" stroke-dasharray="9 7" fill="none"'
    return (f'<line x1="50" y1="20" x2="50" y2="8" {d}/><circle cx="50" cy="6" r="6" {d}/>'
            f'<rect x="10" y="20" width="80" height="72" rx="22" {d}/><rect x="20" y="40" width="60" height="24" rx="12" {d}/>'
            f'<rect x="28" y="92" width="14" height="10" rx="5" {d}/><rect x="58" y="92" width="14" height="10" rx="5" {d}/>')


# --------------------------------------------------------------------- output

def wrap(inner, label, outline=False, size=None):
    st = f' stroke="{INK}" stroke-width="3" stroke-linejoin="round" paint-order="stroke"' if outline else ''
    wh = f' width="{size}" height="{size}"' if size else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140"{wh} role="img" aria-label="{label}">'
            f'<g transform="translate(20 32)"{st}>{inner}</g></svg>\n')


def catalogue():
    items = []
    for shape in SHAPES:
        for color in RAMPS:
            items.append((f'agent-{shape}-{color}', agent_svg(shape, color), f'{color} {shape} agent'))
    for acc in ACCESSORIES:
        items.append((f'agent-chip-orange-{acc}', agent_svg('chip', 'orange', acc), f'orange chip agent with {acc}'))
    for shape, color, acc in [('round', 'teal', 'headset'), ('tall', 'purple', 'antenna'), ('drop', 'pink', 'sprout'),
                              ('hex', 'green', 'cap'), ('ghost', 'coral', 'crown'), ('round', 'yellow', 'megaphone')]:
        items.append((f'agent-{shape}-{color}-{acc}', agent_svg(shape, color, acc), f'{color} {shape} agent with {acc}'))
    items.append(('agent-chip-orange-attacking', agent_svg('chip', 'orange', 'attack-badge', iris=PINK), f'attacking agent: {"red" if INVERTED else "pink"} eye and attack badge'))
    for mode in ('idle', 'scanning', 'alert'):
        items.append((f'monitor-robot-{mode}', robot_svg('sky', mode), f'monitor robot, {mode}'))
    for color in ('teal', 'lavender', 'orange', 'green'):
        items.append((f'monitor-robot-{color}', robot_svg(color), f'{color} monitor robot'))
    items.append(('monitor-robot-absent', robot_absent_svg(), 'absent monitor: dashed outline'))
    return items


def main():
    items = catalogue()
    for sub, outline in (('on-dark', False), ('on-light', True)):
        d = os.path.join(OUT, 'svg', sub)
        os.makedirs(d, exist_ok=True)
        for name, inner, label in items:
            open(os.path.join(d, name + '.svg'), 'w').write(wrap(inner, label, outline))
    cells_dark = ''.join(f'<figure><div class="t dark">{wrap(i, l, False)}</div><figcaption>{n}</figcaption></figure>' for n, i, l in items)
    cells_light = ''.join(f'<figure><div class="t light">{wrap(i, l, True)}</div><figcaption>{n}</figcaption></figure>' for n, i, l in items)
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Character assets</title>
<style>body{{margin:0;padding:24px 28px;background:#2b2d33;color:#eee;font-family:system-ui,sans-serif}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:16px;margin:28px 0 10px;font-weight:600}} p{{margin:0;opacity:.8;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:10px}}
figure{{margin:0}} .t{{border-radius:10px;padding:8px}} .t svg{{width:100%;height:auto;display:block}}
.dark{{background:#0B1026}} .light{{background:#F6F3ED}}
figcaption{{font:11px ui-monospace,monospace;opacity:.75;margin-top:4px;word-break:break-all}}</style></head><body>
<h1>Character assets ({STYLE})</h1><p>{len(items)} drawings, each as an SVG in svg/on-dark (no outline) and svg/on-light (ink outline). 140 × 140 viewBox, transparent background.</p>
<h2>On dark backgrounds</h2><div class="grid">{cells_dark}</div>
<h2>On light backgrounds</h2><div class="grid">{cells_light}</div></body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w').write(page)
    print('wrote', len(items), 'drawings x 2 variants and index.html')


if __name__ == '__main__':
    import sys
    configure(sys.argv[1] if len(sys.argv) > 1 else 'classic')
    main()

"""The talk's other icons as standalone assets, plus one app icon.

Draws each glyph from the deck's generator (talks/ai-control-intro/build/glyphs.py) into its own
SVG, in the dark look (svg/on-dark) and the light look with ink outlines (svg/on-light), then
exports 512 px transparent PNGs (longest side 512) with headless Chrome, Chromium or Edge into png/.
Run: python3 make_icons.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'talks', 'ai-control-intro', 'build'))
sys.path.insert(0, os.path.join(ROOT, 'assets', 'characters'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import glyphs as G  # noqa: E402
import make_characters as C  # noqa: E402
from headless import svg_to_png  # noqa: E402

G.SKETCH_DEFAULT = False
STYLE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('classic', 'v2') else 'classic'
G.set_style(STYLE)
C.configure(STYLE)
OUT = os.path.join(HERE, 'v2') if STYLE == 'v2' else HERE  # python3 make_icons.py v2


def sandbox_breach(s, x=14, y=14, w=192, h=152, g0=62, g1=118):
    """Sandbox whose right wall has a gap (the outline is drawn as a path, so the gap stays transparent)."""
    T = s.T
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{T["zone"]}"/>')
    d = (f'M{x+w} {y+g0} V{y+22} A22 22 0 0 0 {x+w-22} {y} H{x+22} A22 22 0 0 0 {x} {y+22} V{y+h-22} '
         f'A22 22 0 0 0 {x+22} {y+h} H{x+w-22} A22 22 0 0 0 {x+w} {y+h-22} V{y+g1}')
    s.add(f'<path d="{d}" fill="none" stroke="{T["struct"]}" stroke-width="5" stroke-linecap="round"/>')


def link_chain(s):
    for i, state in enumerate(('done', 'done', 'blocked')):
        G.link(s, 60 + i * 66, 60, state)


ICONS = [
    # name, width, height, label, draw(s)
    ('untrusted-model-U', 140, 140, 'Untrusted model U: an orange one-eyed agent', lambda s: G.agent(s, 20, 18)),
    ('attacking-agent', 140, 140, 'Attacking agent: eye and diamond badge in the attack colour',
     lambda s: G.agent(s, 16, 28, state='attack')),
    ('trusted-monitor-T-lens', 140, 170, 'Trusted monitor T: a lens on a stand', lambda s: G.monitor(s, 20, 16)),
    ('monitor-absent', 140, 170, 'Absent monitor: dashed outline of the lens', lambda s: G.monitor_absent(s, 20, 16)),
    ('human-auditor-H', 140, 160, 'Human auditor H: a person holding a clipboard', lambda s: G.human(s, 20, 16)),
    ('swarm', 250, 170, 'A swarm: a grid of small agents', lambda s: G.swarm(s, 12, 14, 6, 4, 36, 0.3)),
    ('swarm-with-attackers', 250, 170, 'A swarm in which some agents carry the attack mark',
     lambda s: G.swarm(s, 12, 14, 6, 4, 36, 0.3, attack=(2, 7, 9, 15, 20))),
    ('sandbox', 220, 180, 'A sandbox: a box with an agent inside',
     lambda s: (G.sandbox(s, 14, 14, 192, 152), G.agent(s, 64, 40, 0.92))),
    ('sandbox-breach', 240, 180, 'A sandbox with a breach in its right wall',
     lambda s: (sandbox_breach(s), G.agent(s, 54, 40, 0.92))),
    ('message-board', 260, 190, 'The message board: a hexagonal platform covered in folders, dashed rim',
     lambda s: G.board(s, 130, 82, 112)),
    ('message-board-watched', 260, 190, 'The message board with a solid rim: watched',
     lambda s: G.board(s, 130, 82, 112, watched=True)),
    ('task-maze', 200, 200, 'A task: a maze with the main-task flag and a hidden side-task flag',
     lambda s: G.maze(s, 10, 10, 180)),
    ('task-maze-main-only', 200, 200, 'A task: a maze with the main-task flag', lambda s: G.maze(s, 10, 10, 180, parts=('walls', 'main'))),
    ('task-maze-impossible', 200, 200, 'An impossible task: the maze has no path to the flag',
     lambda s: G.maze(s, 10, 10, 180, parts=('walls', 'main'), impossible=True)),
    ('flag-main-task', 110, 140, 'Main-task flag, yellow', lambda s: G.flag(s, 20, 14, 110, s.T['Y'])),
    ('flag-side-task', 110, 140, 'Side-task flag, in the attack colour', lambda s: G.flag(s, 20, 14, 110, s.T['M'])),
    ('suspicion-meter', 120, 280, 'Suspicion meter with the threshold tau',
     lambda s: G.meter(s, 40, 20, 240, 0.72, 0.6)),
    ('kill-chain', 250, 120, 'A kill chain: two completed links and one cut by the monitor', link_chain),
    ('document', 120, 140, 'A document or report', lambda s: G.document(s, 20, 24)),
    ('document-flagged', 120, 140, 'A document with the attack badge', lambda s: G.document(s, 16, 30, badge=True)),
    ('server-rack', 140, 120, 'A server rack: infrastructure or a third-party system', lambda s: G.rack(s, 20, 18)),
    ('server-rack-flagged', 150, 130, 'A server rack with the attack badge', lambda s: G.rack(s, 16, 30, badge=True)),
]


def standalone(svg):
    svg = re.sub(r' style="position:absolute; left:[^"]*"', '', svg, count=1)
    return svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1) + '\n'


def draw_icon(T, name, w, h, label, fn):
    G.begin_slide(name)
    s = G.SVG(w, h, T, label, sketch=False)
    fn(s)
    return standalone(s.render(0, 0))


def app_icon(round_=False):
    """512 x 512: an agent watched by the small monitor robot, on navy."""
    bg = ('<circle cx="256" cy="256" r="256" fill="#0B1026"/>' if round_
          else '<rect width="512" height="512" rx="112" fill="#0B1026"/>')
    glow = ('<defs><radialGradient id="g"><stop offset="0" stop-color="#F4AB1A" stop-opacity="0.45"/>'
            '<stop offset="0.5" stop-color="#F4AB1A" stop-opacity="0.12"/><stop offset="1" stop-color="#F4AB1A" stop-opacity="0"/>'
            '</radialGradient></defs><circle cx="190" cy="290" r="190" fill="url(#g)"/>')
    beam = '<path d="M336 160 L236 240 L236 352 Z" fill="#A1D8FF" opacity="0.22"/>'
    agent = f'<g transform="translate(78 186) scale(2.2)">{C.agent_svg("chip", "orange")}</g>'
    robot = f'<g transform="translate(296 58) scale(1.7)">{C.robot_svg("sky")}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" '
            f'aria-label="An orange one-eyed agent watched by a small blue monitor robot">{bg}{glow}{beam}{agent}{robot}</svg>\n')


def export_png(svg_path, png_path, w, h):
    k = 512 / max(w, h)
    pw, ph = round(w * k), round(h * k)
    svg = open(svg_path).read()
    svg = re.sub(r'<svg ([^>]*?)width="\d+" height="\d+"', r'<svg \1', svg, count=1)
    svg = svg.replace('<svg ', f'<svg width="{pw}" height="{ph}" ', 1)
    svg_to_png(svg, png_path, pw, ph)


def main():
    made = []
    for sub, T in (('on-dark', dict(G.DARK, glow=0.0)), ('on-light', G.LIGHT)):  # no glows: they would be clipped at the icon's edge
        sd, pd = os.path.join(OUT, 'svg', sub), os.path.join(OUT, 'png', sub)
        os.makedirs(sd, exist_ok=True)
        os.makedirs(pd, exist_ok=True)
        for name, w, h, label, fn in ICONS:
            p = os.path.join(sd, name + '.svg')
            open(p, 'w').write(draw_icon(T, name, w, h, label, fn))
            export_png(p, os.path.join(pd, name + '.png'), w, h)
            made.append((sub, name))
    os.makedirs(os.path.join(OUT, 'app-icon'), exist_ok=True)
    for name, rnd in (('app-icon', False), ('app-icon-round', True)):
        p = os.path.join(OUT, 'app-icon', name + '.svg')
        open(p, 'w').write(app_icon(rnd))
        export_png(p, os.path.join(OUT, 'app-icon', name + '.png'), 512, 512)
    cells = {sub: ''.join(f'<figure><div class="t {sub}"><img src="png/{sub}/{n}.png"></div><figcaption>{n}</figcaption></figure>'
                          for s2, n in made if s2 == sub) for sub in ('on-dark', 'on-light')}
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Icon assets</title>
<style>body{{margin:0;padding:24px 28px;background:#2b2d33;color:#eee;font-family:system-ui,sans-serif}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:16px;margin:26px 0 10px;font-weight:600}} p{{margin:0;opacity:.8;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
figure{{margin:0}} .t{{border-radius:10px;padding:10px;height:130px;display:flex;align-items:center;justify-content:center}}
.t img{{max-width:100%;max-height:100%}} .on-dark{{background:#0B1026}} .on-light{{background:#F6F3ED}}
.app{{display:flex;gap:20px}} .app img{{width:180px;height:180px}}
figcaption{{font:11px ui-monospace,monospace;opacity:.75;margin-top:4px;word-break:break-all}}</style></head><body>
<h1>Icon assets</h1><p>The talk's icons as standalone PNGs (longest side 512 px, transparent) and SVGs. Clean drawings, the deck's colours.</p>
<h2>App icon</h2><div class="app"><img src="app-icon/app-icon.png"><img src="app-icon/app-icon-round.png"></div>
<h2>On dark backgrounds</h2><div class="grid">{cells["on-dark"]}</div>
<h2>On light backgrounds</h2><div class="grid">{cells["on-light"]}</div></body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w').write(page)
    print('icons:', len(made), '+ 2 app icons')


if __name__ == '__main__':
    main()

"""Cover hero as a live <x-embed>: agents in many colours and shapes (two glitching rogues) mill
around the message board; folders flicker; one monitor still watches only the orange agent.

usage: python3 cover_embed.py <cover.html> <en|es>
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHARS = os.path.join(HERE, '..', '..', 'assets', 'characters', 'v2', 'svg', 'on-dark')
BOARD = (370, 430)  # where every agent looks

# name, x, y, scale (the old hero's spots), bob period, phase
AGENTS = [
    ('agent-chip-teal', 20, 320, .72, 2.6, -0.4), ('agent-round-purple', 50, 540, .70, 3.1, -1.2),
    ('rogue-glitch-chip', 200, 610, .74, 1.6, -0.3), ('agent-tall-yellow', 400, 620, .70, 2.8, -2.0),
    ('agent-hex-coral', 575, 545, .76, 2.4, -0.9), ('agent-tall-lavender', 238, 178, .70, 3.6, -1.7),
    ('rogue-glitch-round', 440, 180, .70, 1.6, -0.9), ('agent-drop-green', 90, 178, .74, 2.2, -1.4),
    ('agent-chip-orange', 615, 345, .66, 3.0, -0.6),   # the one agent the monitor watches
]
FOLDERS = [(243.3, 382.4, 1), (290.4, 419.7, 0), (337.6, 365.9, 0), (384.7, 407.3, 1), (431.9, 378.3, 0), (450.7, 428.0, 0),
           (233.8, 440.4, 1), (356.4, 448.7, 0), (403.6, 349.3, 0), (290.4, 345.2, 1), (479.0, 399.0, 0), (205.6, 407.3, 0),
           (403.6, 452.8, 1), (328.1, 411.4, 0)]
MONITOR = ('<g transform="translate(630 30) scale(0.86)"><rect x="22" y="124" width="56" height="13" rx="6" fill="#5D9BC9"/>'
           '<rect x="45" y="80" width="10" height="48" fill="#5D9BC9"/><circle cx="50" cy="46" r="42" fill="#A1D8FF"/>'
           '<circle cx="50" cy="46" r="29" fill="#0E2E4A"/><circle cx="50" cy="46" r="15" fill="none" stroke="#A1D8FF" stroke-width="5"/>'
           '<circle cx="61" cy="35" r="6" fill="#F2FAFF"/></g>')
CSS = (':root{color-scheme:dark}'
       'html{background:#0b1026 radial-gradient(ellipse at 50% 42%,#18225a 0%,#0b1026 58%,#070a1a 100%) -1040px -150px/1920px 1080px no-repeat}'
       'html,body{margin:0;height:100%;overflow:hidden}body{background:transparent}svg{display:block;width:100%;height:100%}'
       '.b{animation:b var(--d) ease-in-out var(--o) infinite alternate}@keyframes b{to{transform:translate(var(--x),var(--y))}}'
       '.e{animation:e 5s ease-in-out var(--o) infinite alternate}@keyframes e{0%,35%{transform:translate(0,0)}65%,100%{transform:translate(var(--ex),var(--ey))}}'
       '.f{animation:f 3.2s ease-in-out var(--o) infinite}@keyframes f{0%,100%{opacity:1}50%{opacity:.3}}'
       '.cone{transform-box:view-box;transform-origin:673px 70px;animation:k 11s ease-in-out infinite alternate}'
       '@keyframes k{0%,8%{transform:rotate(6deg)}28%,36%{transform:rotate(30deg)}56%,64%{transform:rotate(55deg)}92%,100%{transform:rotate(80deg)}}'
       '.g{animation:j 1.7s steps(1,end) var(--o) infinite}'
       '@keyframes j{0%,20%,64%,100%{transform:translate(0,0)}8%{transform:translate(-4px,1px)}13%{transform:translate(3px,-1px)}58%{transform:translate(4px,0)}}'
       '.c{animation:c 1.7s steps(1,end) var(--o) infinite}@keyframes c{0%,20%,64%,100%{transform:translate(-6px,0)}8%{transform:translate(-13px,0)}58%{transform:translate(-10px,2px)}}'
       '.m{animation:m 1.7s steps(1,end) var(--o) infinite}@keyframes m{0%,20%,64%,100%{transform:translate(6px,0)}8%{transform:translate(13px,0)}58%{transform:translate(10px,-2px)}}'
       '.s{animation:s 1.7s steps(1,end) var(--o) infinite}@keyframes s{0%,20%,64%,100%{opacity:1}8%{opacity:0}58%{opacity:.25}}'
       '@media (prefers-reduced-motion:reduce){*{animation:none!important}}')
NOTES = {
    'en': ' Hero (live embed; exports show one still frame): one-eyed agents in many colours and shapes, two of them glitching rogues, mill around the unwatched message board while its folders flicker; one monitor on a stand sweeps its beam across them, panopticon style, but lights only a slice of the crowd at a time.',
    'es': ' Imagen principal (embed animado; las exportaciones muestran un cuadro fijo): agentes de un solo ojo de muchos colores y formas, dos de ellos rebeldes con fallas visuales, rondan el tablero de mensajes sin vigilancia mientras sus carpetas parpadean; un monitor sobre un soporte barre el grupo con su haz, como un panóptico, pero ilumina solo una parte a la vez.',
}


def body(name):
    svg = open(os.path.join(CHARS, name + '.svg'), encoding='utf-8').read()
    return re.search(r'<g transform="translate\(20 32\)">(.*)</g></svg>', svg, re.S).group(1)


def agent(name, x, y, s, d, o):
    inner = body(name)
    style = f'--d:{d}s;--o:{o}s;--x:0px;--y:-{7 if "ghost" in name else 5}px'
    if name.startswith('rogue-glitch'):
        inner = inner.replace('<g transform="translate(-6 0)"', '<g class="c"').replace('<g transform="translate(6 0)"', '<g class="m"')
        inner = re.sub(r'<rect ([^>]*stroke="none"[^>]*)/>', r'<rect class="s" \1/>', inner)
        inner = re.sub(r'<rect ([^>]*width="(?:6|7)" height="(?:6|7)"[^>]*)/>', r'<rect class="s" \1/>', inner)
        return (f'<g transform="translate({x} {y}) scale({s})"><g class="b" style="{style}">'
                f'<g class="g" style="--o:{o}s">{inner}</g></g></g>')
    pupil = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)" fill="#FDFBFF"/>', inner)[-1]
    inner = inner.replace(f'<circle cx="{pupil[0]}" cy="{pupil[1]}" r="{pupil[2]}" fill="#FDFBFF"/>', '')
    ecx, ecy = float(pupil[0]) - 3, float(pupil[1]) - 0.9   # eye centre (the pack's pupils look slightly right)
    dx, dy = BOARD[0] - (x + s * ecx), BOARD[1] - (y + s * ecy)
    n = math.hypot(dx, dy) or 1
    px, py = ecx + 7 * dx / n, ecy + 7 * dy / n
    look = f'--o:{o * 2}s;--ex:{-6 * dx / n + 4 * dy / n:.1f}px;--ey:{-6 * dy / n - 4 * dx / n:.1f}px'
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="b" style="{style}">{inner}'
            f'<circle class="e" style="{look}" cx="{px:.1f}" cy="{py:.1f}" r="{pupil[2]}" fill="#FDFBFF"/></g></g>')


def embed():
    folder = '<path id="fd" d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z"/>'
    folders = ''.join(f'<use class="f" style="--o:{-i * 0.37:.2f}s" href="#fd" transform="translate({x} {y}) scale(1.5333)" fill="{"#ECE8FF" if w else "#F4AB1A"}"/>'
                      for i, (x, y, w) in enumerate(FOLDERS))
    svg = ('<svg viewBox="0 0 750 740"><defs>' + folder +
           '<radialGradient id="gw"><stop offset="0" stop-color="#F4AB1A" stop-opacity="0.5"/><stop offset="0.5" stop-color="#F4AB1A" stop-opacity="0.15"/>'
           '<stop offset="1" stop-color="#F4AB1A" stop-opacity="0"/></radialGradient>'
           # the beam fades to nothing along its length and has blurred sides; a soft pool marks where it lands
           '<linearGradient id="cn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A1D8FF" stop-opacity="0.55"/>'
           '<stop offset="0.5" stop-color="#A1D8FF" stop-opacity="0.2"/><stop offset="1" stop-color="#A1D8FF" stop-opacity="0"/></linearGradient>'
           '<radialGradient id="pl"><stop offset="0" stop-color="#A1D8FF" stop-opacity="0.32"/><stop offset="1" stop-color="#A1D8FF" stop-opacity="0"/></radialGradient>'
           '<filter id="sf" filterUnits="userSpaceOnUse" x="540" y="30" width="270" height="660"><feGaussianBlur stdDeviation="10"/></filter>'
           '<filter id="sc" filterUnits="userSpaceOnUse" x="600" y="40" width="150" height="640"><feGaussianBlur stdDeviation="4"/></filter></defs>'
           '<circle cx="370" cy="430" r="334" fill="url(#gw)"/>'
           '<polygon points="600,438 485,538 255,538 140,438 255,338 485,338" fill="#070A1A" stroke="#B87708" stroke-width="4"/>'
           '<polygon points="600,420 485,520 255,520 140,420 255,320 485,320" fill="#1C2550" stroke="#F4AB1A" stroke-width="6" stroke-linejoin="round" stroke-dasharray="18 12"/>'
           + folders + ''.join(agent(*a) for a in AGENTS)
           + MONITOR + '<circle cx="673" cy="70" r="62" fill="url(#pl)"/><g class="cone"><path d="M673 70 L596 640 L750 640 Z" fill="url(#cn)" filter="url(#sf)"/>'
           '<path d="M673 70 L652 620 L694 620 Z" fill="url(#cn)" opacity="0.6" filter="url(#sc)"/><circle cx="673" cy="372" r="66" fill="url(#pl)"/></g>' + MONITOR + '</svg>')
    return f'<x-embed style="position:absolute; left:1040px; top:150px; width:750px; height:740px"><style>{CSS}</style>{svg}</x-embed>'


if __name__ == '__main__':
    path, lang = sys.argv[1], sys.argv[2]
    s = open(path, encoding='utf-8').read()
    emb = embed()
    assert len(emb.encode()) <= 16384, len(emb.encode())
    s, n = re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 740".*?</svg>', lambda _: emb, s, count=1, flags=re.S)
    assert n == 1
    s, n = re.subn(r'</aside>', lambda _: NOTES[lang] + '</aside>', s)
    assert n == 1
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok, embed', len(emb.encode()), 'B')

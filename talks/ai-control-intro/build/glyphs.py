"""Glyph library and tokens for the ai-control-intro deck specimen.

Every recurring entity is drawn by exactly one function here, so each
entity looks the same every time it appears. Geometry is in canonical
units; callers place it with translate + scale. Output is plain SVG with
presentation attributes only (no <style>, no class, no <text>, no var()),
so it survives the Slides format.
"""
import math
import re

DARK = dict(
    name='dark',
    bg='#0B1026', deep='#070A1A', surface='#151C3D', surface2='#1C2550',
    zone='#10173A', zoneB='#151B45', rule='#2B3567', rule2='#3A4478', struct='#8A93C9',
    text='#F2F0FF', muted='#B8BEE0',
    U='#F4AB1A', Ushade='#B87708', Ulight='#FFD98A',
    T='#A1D8FF', Tshade='#5D9BC9', Tglass='#0E2E4A', Tlight='#F2FAFF',
    H='#ECE8FF', Hshade='#A69EE0',
    M='#DA86B4', G='#00996F', Y='#FFF251', infra='#A3AADB', infraDot='#0B1026',
    hl='#FFF251', sclera='#FDFBFF', iris='#0B1026', paper='#FDFBFF', ink='#0B1026',
    page='#ECE8FF', docline='#4A5590', outline=None, glow=0.5,
    pillfill=dict(U='#F4AB1A', T='#A1D8FF', H='#ECE8FF', M='#DA86B4', Y='#FFF251', S='#1C2550', I='#A3AADB'),
    pilltext=dict(U='#0B1026', T='#0B1026', H='#0B1026', M='#0B1026', Y='#0B1026', S='#F2F0FF', I='#0B1026'),
)

LIGHT = dict(
    name='light',
    bg='#F6F3ED', deep='#EEE9DF', surface='#FFFDF8', surface2='#EEE7DA',
    zone='#EFEAE1', zoneB='#E9E6EF', rule='#D6CFC3', rule2='#CFC7BA', struct='#5C6577',
    text='#1A2230', muted='#3F4858',
    U='#E69F00', Ushade='#8A5600', Ulight='#F8D58A',
    T='#85CFFF', Tshade='#00577D', Tglass='#E3F3FC', Tlight='#FFFDF8',
    H='#3A4558', Hshade='#9AA3B2',
    M='#CC79A7', G='#007A58', Y='#F0E442', infra='#AEB5C4', infraDot='#1A2230',
    hl='#F0E442', sclera='#FFFDF8', iris='#1A2230', paper='#FFFDF8', ink='#1A2230',
    page='#FFFDF8', docline='#9AA3B2', outline='#1A2230', glow=0.0,
    pillfill=dict(U='#E69F00', T='#85CFFF', H='#3A4558', M='#8A3D69', Y='#F0E442', S='#EEE7DA', I='#AEB5C4'),
    pilltext=dict(U='#1A2230', T='#1A2230', H='#FFFDF8', M='#FFFDF8', Y='#1A2230', S='#1A2230', I='#1A2230'),
)

FONT_D = "'Outfit', 'Trebuchet MS', sans-serif"
FONT_M = "'JetBrains Mono', 'Courier New', monospace"


SKETCH_DEFAULT = True

# Look of the cast. v2 (chosen 2026-10-07): agents have a black eye with a white centre, and the
# attack colour is red. 'classic' restores the first look (white eye, reddish-purple attack colour).
EYE_INVERTED = True
ATTACK = {'v2': {'dark': '#FF3B5C', 'light': '#D7263D', 'light_pill': '#B3172E'},
          'classic': {'dark': '#DA86B4', 'light': '#CC79A7', 'light_pill': '#8A3D69'}}


def set_style(style):
    """Switch every glyph between the 'v2' and 'classic' looks."""
    global EYE_INVERTED
    EYE_INVERTED = style == 'v2'
    a = ATTACK[style]
    DARK['M'] = DARK['pillfill']['M'] = a['dark']
    LIGHT['M'] = a['light']
    LIGHT['pillfill']['M'] = a['light_pill']


def begin_slide(sid):
    """Call once at the start of each slide builder. Every SVG id on the slide then starts with the
    slide id, so gradients, markers and filters never collide across slides built in parallel."""
    SVG.prefix = re.sub(r'[^A-Za-z0-9]', '', sid) + 'x'
    SVG.count = 0


class SVG:
    """One standalone inline SVG. Ids carry a per-SVG prefix so many SVGs can
    share one HTML page without id collisions."""
    count = 0
    prefix = 'g'

    def __init__(self, w, h, T, label, sketch=None, wobble=7):
        """sketch=None follows SKETCH_DEFAULT (the speaker chose sketch rendering for the whole deck).
        Pass sketch=False for QR codes, which must stay crisp to scan. Use a smaller wobble (2-3)
        for SVGs full of tiny glyphs such as swarm grids, so they do not melt into blobs."""
        SVG.count += 1
        self.pid = f"{SVG.prefix}{SVG.count}"
        self.sketch = SKETCH_DEFAULT if sketch is None else sketch
        self.wobble = wobble
        self.w, self.h, self.T, self.label = w, h, T, label
        self.defs, self.body, self.under, self.k, self.markers = [], [], [], 0, {}

    def uid(self):
        self.k += 1
        return f"{self.pid}i{self.k}"

    def add(self, s):
        self.body.append(s)

    def g(self, x, y, sc, inner):
        """Place a canonical glyph. Light variant adds a 4 px (canvas) ink outline."""
        o = self.T['outline']
        st = (f' stroke="{o}" stroke-width="{4/sc:.2f}" stroke-linejoin="round"' if o else '')
        self.add(f'<g transform="translate({x:.1f} {y:.1f}) scale({sc})"{st}>{inner}</g>')

    def glow(self, cx, cy, r, color, op=None):
        """Soft halo: a radial-gradient disc. The light variant has no glows."""
        op = self.T['glow'] if op is None else op * (1 if self.T['glow'] else 0)
        if op <= 0:
            return
        i = self.uid()
        self.defs.append(
            f'<radialGradient id="{i}"><stop offset="0" stop-color="{color}" stop-opacity="{op}"/>'
            f'<stop offset="0.5" stop-color="{color}" stop-opacity="{op*0.3:.3f}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        # glows sit under the sketch filter so their soft edge stays round
        self.under.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#{i})"/>')

    def marker(self, color):
        if color not in self.markers:
            i = self.uid()
            self.markers[color] = i
            self.defs.append(
                f'<marker id="{i}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" '
                f'overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{color}"/></marker>')
        return self.markers[color]

    def arrow(self, pts, color, w=5, head=True, dash=None):
        d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
        m = f' marker-end="url(#{self.marker(color)})"' if head else ''
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
                 f'stroke-linecap="round" stroke-linejoin="round"{da}{m}/>')

    def render(self, x, y, attrs=''):
        defs = list(self.defs)
        body = ''.join(self.body)
        if self.sketch:
            i = self.uid()
            defs.append(f'<filter id="{i}" x="-5%" y="-5%" width="110%" height="110%">'
                        f'<feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="7" result="n"/>'
                        f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{self.wobble}" xChannelSelector="R" '
                        f'yChannelSelector="G"/></filter>')
            body = f'<g filter="url(#{i})">{body}</g>'
        body = ''.join(self.under) + body
        d = f'<defs>{"".join(defs)}</defs>' if defs else ''
        return (f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{self.label}" style="position:absolute; left:{x}px; top:{y}px"{attrs}>'
                f'{d}{body}</svg>')


def look_at(ax, ay, tx, ty):
    dx, dy = tx - ax, ty - ay
    d = math.hypot(dx, dy) or 1
    return (dx / d, dy / d)


# ---- U: the agent, one instance of the untrusted model -----------------
# Canonical box 100 x 104. A one-eyed microchip: squircle body, two pins on
# each side, two pin feet. U the model is the same glyph drawn large.
def agent(s, x, y, sc=1.0, state='normal', look=(0, 0), tiny=False):
    T = s.T
    g = []
    if not tiny:
        for py in (34, 54):
            g.append(f'<rect x="0" y="{py}" width="12" height="9" rx="3" fill="{T["Ushade"]}"/>')
            g.append(f'<rect x="88" y="{py}" width="12" height="9" rx="3" fill="{T["Ushade"]}"/>')
        g.append(f'<rect x="28" y="84" width="12" height="18" rx="5" fill="{T["Ushade"]}"/>')
        g.append(f'<rect x="60" y="84" width="12" height="18" rx="5" fill="{T["Ushade"]}"/>')
    g.append(f'<rect x="8" y="6" width="84" height="84" rx="28" fill="{T["U"]}"/>')
    if not tiny:
        g.append(f'<ellipse cx="30" cy="21" rx="11" ry="6" fill="{T["Ulight"]}" stroke="none"/>')
    lx, ly = look
    if EYE_INVERTED:  # v2: black eye, white centre; an attacking agent's centre turns the attack red
        g.append(f'<circle cx="50" cy="48" r="24" fill="{T["iris"]}"/>')
        inner = T['M'] if state == 'attack' else T['sclera']
        g.append(f'<circle cx="{50+lx*9:.1f}" cy="{48+ly*9:.1f}" r="12" fill="{inner}" stroke="none"/>')
    else:
        g.append(f'<circle cx="50" cy="48" r="24" fill="{T["sclera"]}"/>')
        iris = T['M'] if state == 'attack' else T['iris']
        g.append(f'<circle cx="{50+lx*9:.1f}" cy="{48+ly*9:.1f}" r="12" fill="{iris}" stroke="none"/>')
        if not tiny:
            g.append(f'<circle cx="{54+lx*9:.1f}" cy="{44+ly*9:.1f}" r="4" fill="{T["sclera"]}" stroke="none"/>')
    if state == 'attack':  # attack mark: a reddish-purple diamond badge (shape + colour)
        g.append(f'<path d="M86 -8 L102 8 L86 24 L70 8 Z" fill="{T["M"]}" stroke="{T["bg"] if not T["outline"] else T["outline"]}" '
                 f'stroke-width="5" stroke-linejoin="round"/>')
    s.g(x, y, sc, ''.join(g))


# ---- T: the trusted monitor, a lens on a stand -------------------------
# Canonical box 100 x 138. Lens centre at (50, 46).
def monitor(s, x, y, sc=1.0):
    T = s.T
    g = [
        f'<rect x="22" y="124" width="56" height="13" rx="6" fill="{T["Tshade"]}"/>',
        f'<rect x="45" y="80" width="10" height="48" fill="{T["Tshade"]}"/>',
        f'<circle cx="50" cy="46" r="42" fill="{T["T"]}"/>',
        f'<circle cx="50" cy="46" r="29" fill="{T["Tglass"]}"/>',
        f'<circle cx="50" cy="46" r="15" fill="none" stroke="{T["T"] if not T["outline"] else T["Tshade"]}" stroke-width="5"/>',
        f'<circle cx="61" cy="35" r="6" fill="{T["Tlight"]}" stroke="none"/>',
    ]
    s.g(x, y, sc, ''.join(g))
    return (x + 50 * sc, y + 46 * sc)


def beam(s, lx, ly, tx, ty0, ty1, down=False):
    """Translucent scan cone from a lens centre to a target span: vertical span at x=tx,
    or with down=True a horizontal span from tx to ty0 at height ty1."""
    T = s.T
    i = s.uid()
    x2 = 1 if tx > lx else 0
    col = T['T'] if T['name'] == 'dark' else T['Tshade']
    s.defs.append(f'<linearGradient id="{i}" x1="{1-x2}" y1="0" x2="{x2}" y2="0">'
                  f'<stop offset="0" stop-color="{col}" stop-opacity="0.45"/>'
                  f'<stop offset="1" stop-color="{col}" stop-opacity="0.06"/></linearGradient>')
    if down:
        s.defs[-1] = (f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1">'
                      f'<stop offset="0" stop-color="{col}" stop-opacity="0.45"/>'
                      f'<stop offset="1" stop-color="{col}" stop-opacity="0.06"/></linearGradient>')
        s.add(f'<path d="M{lx:.0f} {ly:.0f} L{tx:.0f} {ty1:.0f} L{ty0:.0f} {ty1:.0f} Z" fill="url(#{i})"/>')
        return
    s.add(f'<path d="M{lx:.0f} {ly:.0f} L{tx:.0f} {ty0:.0f} L{tx:.0f} {ty1:.0f} Z" fill="url(#{i})"/>')


# ---- H: the human auditor, a bust holding a clipboard ------------------
# Canonical box 100 x 128.
def human(s, x, y, sc=1.0):
    T = s.T
    g = [
        f'<circle cx="44" cy="30" r="24" fill="{T["H"]}"/>',
        f'<path d="M4 128 C4 92 22 66 44 66 C66 66 84 92 84 128 Z" fill="{T["H"]}"/>',
        f'<rect x="56" y="72" width="42" height="54" rx="6" fill="{T["Hshade"]}"/>',
        f'<rect x="62" y="80" width="30" height="40" rx="3" fill="{T["paper"]}" stroke="none"/>',
        f'<rect x="67" y="88" width="20" height="4" rx="2" fill="{T["ink"]}" stroke="none"/>',
        f'<rect x="67" y="97" width="20" height="4" rx="2" fill="{T["ink"]}" stroke="none"/>',
        f'<rect x="67" y="106" width="13" height="4" rx="2" fill="{T["ink"]}" stroke="none"/>',
        f'<rect x="69" y="67" width="16" height="9" rx="3" fill="{T["ink"]}" stroke="none"/>',
    ]
    s.g(x, y, sc, ''.join(g))


# ---- swarm: a grid of tiny agents ---------------------------------------
def swarm(s, x, y, cols, rows, pitch, sc, attack=(), count=None, stagger=True, target=None):
    n = 0
    for r in range(rows):
        for c in range(cols):
            if count is not None and n >= count:
                return
            ax = x + c * pitch + (pitch / 2 if (stagger and r % 2) else 0)
            ay = y + r * pitch
            if target:
                lk = look_at(ax + 50 * sc, ay + 48 * sc, *target)
            else:
                lk = [(0.6, 0), (-0.5, 0.3), (0, 0.6), (0.4, -0.4), (-0.6, -0.2)][(r * 7 + c * 3) % 5]
            agent(s, ax, ay, sc, 'attack' if n in attack else 'normal', lk, tiny=True)
            n += 1


# ---- sandbox: a glowing box ---------------------------------------------
def sandbox(s, x, y, w, h, breach=None, outside=None):
    T = s.T
    if T['glow'] > 0:
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="none" '
              f'stroke="{T["struct"]}" stroke-width="18" opacity="0.15"/>')
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{T["zone"]}" '
          f'stroke="{T["struct"]}" stroke-width="5"/>')
    if breach:  # (y0, y1): a gap in the right wall
        y0, y1 = breach
        s.add(f'<rect x="{x+w-10}" y="{y0}" width="20" height="{y1-y0}" fill="{outside or T["bg"]}"/>')


# ---- message board: a hexagonal platform crowded with folders -----------
FOLDER_SPOTS = [(-0.55, -0.25), (-0.3, 0.2), (-0.05, -0.45), (0.2, 0.05), (0.45, -0.3),
                (0.55, 0.3), (-0.6, 0.45), (0.05, 0.55), (0.3, -0.65), (-0.3, -0.7),
                (0.7, -0.05), (-0.75, 0.05), (0.3, 0.6), (-0.1, 0.1)]


def folder(s, x, y, sc, color):
    s.g(x, y, sc, f'<path d="M0 4 Q0 1 3 1 H11 L14 5 H27 Q30 5 30 8 V19 Q30 22 27 22 H3 Q0 22 0 19 Z" '
                  f'fill="{color}"/>')


def board(s, cx, cy, r, watched=False, n=14):
    """Unwatched board: dashed rim. Dashed always means no monitor reads it."""
    T = s.T
    s.glow(cx, cy + 10, r * 1.45, T['U'])
    pts = [(cx + r * math.cos(math.radians(60 * k)), cy + r * 0.5 * math.sin(math.radians(60 * k)))
           for k in range(6)]
    depth = ' '.join(f'{px:.0f},{py+18:.0f}' for px, py in pts)
    top = ' '.join(f'{px:.0f},{py:.0f}' for px, py in pts)
    s.add(f'<polygon points="{depth}" fill="{T["deep"]}" stroke="{T["Ushade"]}" stroke-width="4"/>')
    dash = '' if watched else ' stroke-dasharray="18 12"'
    s.add(f'<polygon points="{top}" fill="{T["surface2"]}" stroke="{T["U"] if not T["outline"] else T["Ushade"]}" '
          f'stroke-width="6" stroke-linejoin="round"{dash}/>')
    fs = r / 150
    for k, (u, v) in enumerate(FOLDER_SPOTS[:n]):
        folder(s, cx + u * r * 0.82 - 15 * fs, cy + v * r * 0.36 - 11 * fs, fs,
               T['U'] if k % 3 else T['H'])


# ---- maze + flags: a task --------------------------------------------------
MAZE_WALLS = [(0, 0, 5, 0), (5, 0, 5, 5), (1, 5, 5, 5), (0, 0, 0, 5),  # outer, entrance bottom-left
              (1, 0, 1, 1), (0, 1, 1, 1),                              # sealed pocket (side task)
              (1, 2, 1, 4), (2, 3, 4, 3), (2, 1, 4, 1), (3, 4, 3, 5), (4, 1, 4, 2), (2, 1, 2, 2)]


def flag(s, x, y, h, color):
    """Flag: pole + pennant. Main task = yellow, side task = reddish purple."""
    T = s.T
    pw = max(5, h * 0.09)
    o = f' stroke="{T["outline"]}" stroke-width="3" stroke-linejoin="round"' if T['outline'] else ''
    s.add(f'<rect x="{x:.0f}" y="{y:.0f}" width="{pw:.0f}" height="{h:.0f}" rx="2" fill="{T["text"]}"/>')
    s.add(f'<path d="M{x+pw:.0f} {y:.0f} L{x+pw+h*0.62:.0f} {y+h*0.22:.0f} L{x+pw:.0f} {y+h*0.44:.0f} Z" '
          f'fill="{color}"{o}/>')


def maze(s, x, y, size, parts=('walls', 'main', 'side'), impossible=False):
    T = s.T
    pad = size * 0.1
    c = (size - 2 * pad) / 5
    ox, oy = x + pad, y + pad
    if 'walls' in parts:
        s.add(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="20" fill="{T["surface"]}" '
              f'stroke="{T["rule2"]}" stroke-width="2"/>')
        walls = list(MAZE_WALLS) + ([(4, 1, 5, 1)] if impossible else [])
        d = ' '.join(f'M{ox+a*c:.0f} {oy+b*c:.0f} L{ox+e*c:.0f} {oy+f*c:.0f}' for a, b, e, f in walls)
        s.add(f'<path d="{d}" fill="none" stroke="{T["struct"]}" stroke-width="{max(5, size/45):.0f}" '
              f'stroke-linecap="round"/>')
        s.add(f'<circle cx="{ox+c*0.5:.0f}" cy="{oy+c*4.5:.0f}" r="{c*0.2:.0f}" fill="{T["U"]}"/>')
    if 'main' in parts:
        flag(s, ox + c * 4.3, oy + c * 0.12, c * 0.74, T['Y'])
    if 'side' in parts:  # hidden: sealed pocket, dashed ring = the monitor does not see it
        s.glow(ox + c * 0.5, oy + c * 0.5, c * 0.9, T['M'])
        s.add(f'<circle cx="{ox+c*0.5:.0f}" cy="{oy+c*0.5:.0f}" r="{c*0.44:.0f}" fill="none" '
              f'stroke="{T["M"]}" stroke-width="4" stroke-dasharray="7 6"/>')
        flag(s, ox + c * 0.36, oy + c * 0.18, c * 0.62, T['M'])


# ---- suspicion meter with threshold tau -----------------------------------
def meter(s, x, y, h, score, tau, w=40):
    """Score rises bottom to top. Zone above tau is tinted H: that work goes to the human."""
    T = s.T
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2:.0f}" fill="{T["surface2"]}" '
          f'stroke="{T["struct"]}" stroke-width="3"/>')
    ty = y + (1 - tau) * h
    s.add(f'<path d="M{x+1.5} {ty:.0f} V{y+w/2:.0f} A{w/2-1.5:.1f} {w/2-1.5:.1f} 0 0 1 {x+w-1.5} {y+w/2:.0f} V{ty:.0f} Z" '
          f'fill="{T["H"]}" opacity="0.3"/>')
    ly = y + (1 - score) * h
    s.add(f'<rect x="{x+8}" y="{ly:.0f}" width="{w-16}" height="{y+h-8-ly:.0f}" rx="{(w-16)/2:.0f}" '
          f'fill="{T["T"] if T["name"]=="dark" else T["Tshade"]}"/>')
    s.add(f'<rect x="{x-18}" y="{ty-4:.0f}" width="{w+36}" height="8" rx="4" fill="{T["text"]}"/>')
    return ty, ly


# ---- kill-chain link ------------------------------------------------------
def link(s, cx, cy, state='done'):
    """A chain link. done = attack colour; blocked = grey link cut by a T-coloured bar."""
    T = s.T
    col = {'done': T['M'], 'pending': T['struct'], 'blocked': T['struct']}[state]
    s.add(f'<rect x="{cx-36}" y="{cy-24}" width="72" height="48" rx="24" fill="{T["bg"]}" '
          f'stroke="{col}" stroke-width="7"/>')
    if state == 'blocked':
        s.add(f'<path d="M{cx+22} {cy-36} L{cx+32} {cy+36}" stroke="{T["T"] if T["name"]=="dark" else T["Tshade"]}" '
              f'stroke-width="9" stroke-linecap="round"/>')


# ---- document / report ------------------------------------------------------
# Canonical box 76 x 96.
def document(s, x, y, sc=1.0, badge=False):
    T = s.T
    g = [f'<path d="M0 0 H56 L76 20 V96 H0 Z" fill="{T["page"]}"/>',
         f'<path d="M56 0 V20 H76 Z" fill="{T["Hshade"]}"/>',
         f'<rect x="12" y="36" width="50" height="7" rx="3" fill="{T["docline"]}" stroke="none"/>',
         f'<rect x="12" y="52" width="50" height="7" rx="3" fill="{T["docline"]}" stroke="none"/>',
         f'<rect x="12" y="68" width="34" height="7" rx="3" fill="{T["docline"]}" stroke="none"/>']
    if badge:
        g.append(f'<path d="M76 -12 L92 4 L76 20 L60 4 Z" fill="{T["M"]}" stroke="{T["outline"] or T["bg"]}" '
                 f'stroke-width="5" stroke-linejoin="round"/>')
    s.g(x, y, sc, ''.join(g))


# ---- infrastructure and third-party systems: a server rack ---------------
# Canonical box 100 x 88 (three units). Neutral colour: systems are not actors.
def rack(s, x, y, sc=1.0, badge=False):
    T = s.T
    g = []
    for i in range(3):
        yy = i * 31
        g.append(f'<rect x="0" y="{yy}" width="100" height="26" rx="6" fill="{T["infra"]}"/>')
        g.append(f'<circle cx="15" cy="{yy+13}" r="4" fill="{T["infraDot"]}" stroke="none"/>')
        g.append(f'<rect x="32" y="{yy+11}" width="54" height="4" rx="2" fill="{T["infraDot"]}" stroke="none"/>')
    if badge:
        g.append(f'<path d="M100 -16 L116 0 L100 16 L84 0 Z" fill="{T["M"]}" stroke="{T["outline"] or T["bg"]}" '
                 f'stroke-width="5" stroke-linejoin="round"/>')
    s.g(x, y, sc, ''.join(g))


def tinyrack(s, x, y):
    T = s.T
    o = f' stroke="{T["outline"]}" stroke-width="2"' if T['outline'] else ''
    s.add(f'<rect x="{x}" y="{y}" width="22" height="26" rx="4" fill="{T["infra"]}"{o}/>'
          f'<rect x="{x+5}" y="{y+8}" width="12" height="3" rx="1.5" fill="{T["infraDot"]}"/>'
          f'<rect x="{x+5}" y="{y+15}" width="12" height="3" rx="1.5" fill="{T["infraDot"]}"/>')


def diamond(s, cx, cy, r, color):
    s.add(f'<path d="M{cx:.0f} {cy-r:.0f} L{cx+r:.0f} {cy:.0f} L{cx:.0f} {cy+r:.0f} L{cx-r:.0f} {cy:.0f} Z" fill="{color}"/>')


# ---- QR ------------------------------------------------------------------
def qr(s, x, y, size, matrix):
    """Dark modules on a light card; the 4-module quiet zone is inside size."""
    T = s.T
    n = len(matrix)
    m = size / (n + 8)
    s.add(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="16" fill="{T["paper"]}"/>')
    d = []
    for r, row in enumerate(matrix):
        c = 0
        while c < n:
            if row[c]:
                start = c
                while c < n and row[c]:
                    c += 1
                d.append(f'M{x+(start+4)*m:.2f} {y+(r+4)*m:.2f}h{(c-start)*m:.2f}v{m:.2f}h{-(c-start)*m:.2f}z')
            else:
                c += 1
    s.add(f'<path d="{"".join(d)}" fill="{T["ink"]}" shape-rendering="crispEdges"/>')


# ---- T absent: the monitor's empty seat ("nobody was watching") --------
def monitor_absent(s, x, y, sc=1.0):
    """Same silhouette as T, drawn only as a dashed struct outline. Dashed = no monitor sees this."""
    T = s.T
    st = f'fill="none" stroke="{T["struct"]}" stroke-width="{4/sc:.2f}" stroke-dasharray="{10/sc:.1f} {8/sc:.1f}"'
    s.add(f'<g transform="translate({x:.1f} {y:.1f}) scale({sc})">'
          f'<rect x="22" y="124" width="56" height="13" rx="6" {st}/>'
          f'<rect x="45" y="88" width="10" height="36" {st}/>'
          f'<circle cx="50" cy="46" r="42" {st}/></g>')


set_style('v2')

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
import json
import os
from glyphs import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'specimen.html')
QR = json.load(open('qr.json'))


# ---------------------------------------------------------------- helpers
def bi(build):
    return f' data-build-in="fade {build}"' if build else ''


def P(text, x, y, w, T, size=48, weight=600, color=None, fam=None, align='left', lh=1.15, extra='', build=None):
    color = color or T['text']
    fam = fam or FONT_D
    return (f'<p{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; font-family:{fam}; '
            f'font-size:{size}px; font-weight:{weight}; line-height:{lh}; color:{color}; text-align:{align}{extra}">'
            f'{text}</p>')


def pw(text):
    return 76 if len(text) == 1 else len(text) * 22 + 52


def PILL(text, x, y, T, role, w=None, build=None):
    w = w or pw(text)
    return (f'<p{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; padding:6px 22px; '
            f'border-radius:999px; background:{T["pillfill"][role]}; color:{T["pilltext"][role]}; '
            f'font-family:{FONT_D}; font-size:40px; font-weight:700; line-height:1.15; text-align:center; '
            f'white-space:nowrap">{text}</p>')


def H2(text, T):
    return (f'<h2 style="position:absolute; left:128px; top:128px; width:1560px; font-family:{FONT_D}; '
            f'font-size:72px; font-weight:700; line-height:1.1; letter-spacing:-1.5px; color:{T["text"]}">{text}</h2>')


def FOOT(num, cite, T):
    """Footer band: slide number left, short citation right (28 px, the one exception to the 40 px floor)."""
    return (f'<p style="position:absolute; left:128px; bottom:64px; width:120px; font-family:{FONT_M}; '
            f'font-size:28px; line-height:1; color:{T["muted"]}">{num}</p>'
            f'<p style="position:absolute; right:128px; bottom:64px; width:1400px; font-family:{FONT_M}; '
            f'font-size:28px; line-height:1; color:{T["muted"]}; text-align:right">{cite}</p>')


def SECTION(sid, T, inner, bg=None, desc=None, transition='fade'):
    bg = bg or T['bg']
    ds = f' data-section="{desc}"' if desc else ''
    return (f'<section id="{sid}" data-transition="{transition}"{ds} style="background:{bg}; '
            f'padding:128px 128px 160px; font-family:{FONT_D}; color:{T["text"]}">{inner}</section>')


def EVIDENCE(x, y, w, T, tab, lines, build=None):
    """Evidence card. The incident is the running example; its source goes in the footer citation."""
    kids = [f'<p style="align-self:flex-start; padding:6px 22px; border-radius:999px; background:{T["pillfill"]["H"]}; '
            f'color:{T["pilltext"]["H"]}; font-family:{FONT_D}; font-size:40px; font-weight:700; '
            f'line-height:1.15">{tab}</p>']
    for kind, text in lines:
        if kind == 'claim':
            kids.append(f'<p style="font-family:{FONT_D}; font-size:48px; font-weight:600; line-height:1.15; '
                        f'color:{T["text"]}">{text}</p>')
        elif kind == 'quote':
            kids.append(f'<p style="font-family:{FONT_D}; font-size:40px; font-style:italic; font-weight:400; '
                        f'line-height:1.25; color:{T["text"]}">{text}</p>')
        elif kind == 'mark':
            kids.append(f'<p style="align-self:flex-start; padding:4px 14px; background:{T["hl"]}; color:{T["ink"]}; '
                        f'font-family:{FONT_D}; font-size:40px; font-weight:600; line-height:1.2">{text}</p>')
    return (f'<div{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; background:{T["surface"]}; '
            f'border:3px solid {T["rule2"]}; border-radius:24px; padding:28px 32px; display:flex; '
            f'flex-direction:column; gap:18px">{"".join(kids)}</div>')


RADIAL = 'radial-gradient(ellipse at 50% 42%, #18225A 0%, #0B1026 58%, #070A1A 100%)'
RADIAL_LIGHT = 'radial-gradient(ellipse at 50% 42%, #FFFDF8 0%, #F6F3ED 58%, #EEE9DF 100%)'


def radial(T):
    """The cover / cold-open / closing background for the current palette."""
    return RADIAL_LIGHT if T['name'] == 'light' else RADIAL


def NOTES(text):
    """Speaker notes: plain text, the section's LAST child, at most 4,000 characters."""
    return f'<aside>{text}</aside>'


# ---------------------------------------------------------------- 1 cold open
def s_cold():
    T = DARK
    sv = SVG(420, 430, T, 'A one-eyed agent looks toward the terminal on its right.')
    sv.glow(210, 215, 205, T['U'])
    agent(sv, 80, 80, 2.6, look=(1, -0.1))
    rows = [f'<p style="font-family:{FONT_M}; font-size:40px; line-height:1.3; color:{T["muted"]}">artifactory · the agents’ board</p>',
            f'<p style="font-family:{FONT_M}; font-size:40px; line-height:1.3; color:{T["text"]}"><span style="color:{T["muted"]}">$</span> ls</p>',
            f'<p style="font-family:{FONT_M}; font-size:40px; line-height:1.3; color:{T["U"]}">zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA/</p>',
            f'<p style="font-family:{FONT_M}; font-size:40px; line-height:1.3; color:{T["text"]}"><span style="color:{T["muted"]}">$</span> _</p>']
    term = (f'<div style="position:absolute; left:560px; top:250px; width:1232px; background:{T["deep"]}; '
            f'border:3px solid {T["rule2"]}; border-radius:24px; padding:32px 36px; display:flex; '
            f'flex-direction:column; gap:10px">{"".join(rows)}</div>')
    inner = (P('8 Jul 2026 · evening', 128, 128, 900, T, 40, 500, T['muted'], FONT_M)
             + sv.render(128, 280) + term
             + P('Isolated agents left each other messages as folder names', 128, 730, 1560, T, 72, 700, lh=1.1,
                 extra='; letter-spacing:-1.5px')
             + FOOT('01', 'first message on the board, 8 Jul 2026 · METR 2026', T))
    return SECTION('cold-open', T, inner, RADIAL, 'Cold open: one moment from the incident'), \
        'Cold open: machine evidence (terminal panel beside an agent), with the first message on the board', None


# ---------------------------------------------------------------- 2 cover
def s_cover():
    T = DARK
    sv = SVG(750, 740, T, 'One-eyed agents gather around a glowing hexagonal message board with a dashed rim; '
                          'a single monitor on a stand watches only one of them.')
    cx, cy = 370, 420
    board(sv, cx, cy, 230)
    spots = [(20, 320, .72), (50, 540, .7), (200, 610, .74), (400, 620, .7), (575, 545, .76),
             (240, 190, .66), (440, 180, .7), (95, 190, .6), (615, 345, .66)]
    for ax, ay, sc in spots:
        agent(sv, ax, ay, sc, look=look_at(ax + 50 * sc, ay + 48 * sc, cx, cy))
    lx, ly = monitor(sv, 630, 30, 0.86)
    beam(sv, lx, ly, 615, 615 + 100 * .66, 345, down=True)
    monitor(sv, 630, 30, 0.86)
    inner = (sv.render(1040, 150)
             + P('SPAR · Fall 2026', 128, 300, 900, T, 40, 500, T['muted'], FONT_M)
             + (f'<h1 style="position:absolute; left:128px; top:360px; width:900px; font-family:{FONT_D}; '
                f'font-size:96px; font-weight:800; line-height:1.05; letter-spacing:-2px; color:{T["text"]}; '
                f'text-shadow:0 0 32px rgba(244,171,26,0.28)">AI control, in fifteen minutes</h1>')
             + P('Useful work from models that may be working against us', 128, 600, 860, T, 48, 400, T['muted'])
             + P('Speaker name · Oct 2026', 128, 780, 860, T, 40, 500, T['muted'], FONT_M))
    return SECTION('cover', T, inner, RADIAL, 'Title'), 'Cover', None


# ---------------------------------------------------------------- 3 cast
def s_cast():
    T = DARK
    out = []
    names = ['untrusted model', 'trusted monitor', 'human auditor']
    for i in range(3):
        x0 = 128 + i * 572
        sv = SVG(520, 330, T, f'{"UTH"[i]}, the {names[i]}.')
        if i == 0:
            sv.glow(260, 165, 170, T['U'])
            agent(sv, 130, 28, 2.6, look=(0.2, 0.1))
        elif i == 1:
            sv.glow(260, 120, 170, T['T'])
            monitor(sv, 160, 18, 2.15)
        else:
            sv.glow(250, 165, 160, T['H'], 0.3)
            human(sv, 150, 26, 2.2)
        out.append(sv.render(x0, 330, bi(i + 1)))
        out.append(PILL('UTH'[i], x0 + 222, 690, T, 'UTH'[i], build=i + 1))
        out.append(P(names[i], x0, 774, 520, T, 48, 600, align='center', build=i + 1))
    inner = (H2('Every control game has the same three players', T) + ''.join(out)
             + FOOT('03', 'Control framing: founding paper, 2023', T))
    return SECTION('cast', T, inner), 'Cast slide: pre-training, one glyph per build (descriptive label shown once)', 3


# ---------------------------------------------------------------- 4 incident map
def s_map():
    T = DARK
    OX, OY = 128, 340
    sv = SVG(1664, 560, T, 'Incident map. Left zone, inside the OpenAI evaluation: about 1,200 agents in isolated '
                           'sandboxes post to a message board on Artifactory. The path breaks through the lab '
                           'boundary to the internet. Right zone, Hugging Face: leaked tokens, then code execution '
                           'on 41 dataset workers, then admin across clusters, under 13 hours after the first code execution on a worker.', wobble=4)
    sv.add(f'<rect x="0" y="0" width="620" height="560" rx="28" fill="{T["zone"]}" stroke="{T["rule2"]}" stroke-width="3"/>')
    sv.add(f'<rect x="860" y="0" width="804" height="560" rx="28" fill="{T["zoneB"]}" stroke="{T["struct"]}" stroke-width="3"/>')
    sandbox(sv, 24, 120, 240, 250, outside=T['zone'])
    swarm(sv, 40, 146, 5, 4, 40, 0.3, target=(440, 245))
    board(sv, 440, 235, 112)
    sv.add(f'<rect x="310" y="318" width="260" height="62" rx="16" fill="{T["infra"]}"/>')
    sv.add(f'<rect x="615" y="205" width="10" height="64" fill="{T["bg"]}"/>')  # breach in the lab boundary
    sv.arrow([(264, 245), (316, 239)], T['M'])
    sv.arrow([(552, 237), (872, 237)], T['M'])
    document(sv, 890, 190, 0.9, badge=True)
    sv.arrow([(962, 237), (1036, 237)], T['M'])
    n = 0
    for r in range(6):
        for c in range(7):
            if n < 41:
                tinyrack(sv, 1050 + c * 30, 140 + r * 34)
            n += 1
    sv.arrow([(1256, 237), (1326, 237)], T['M'])
    for rx_, ry_ in [(1350, 160), (1475, 160), (1412, 262)]:
        rack(sv, rx_, ry_, 0.8, badge=True)
    sv.add(f'<path d="M1040 118 V102 H1580 V118" fill="none" stroke="{T["M"]}" stroke-width="5" stroke-linejoin="round"/>')
    rings = [(1, 352, 444), (2, 740, 237), (3, 900, 444), (4, 1120, 444), (5, 1410, 444)]
    for k, cx, cy in rings:
        link(sv, cx, cy)
    lab = ''.join(P(str(k), OX + cx - 36, OY + cy - 24, 72, T, 40, 800, T['M'], align='center', lh=1.2) for k, cx, cy in rings)
    lab += (P('~1,200<br>agents', OX + 24, OY + 420, 240, T, 40, 600, lh=1.2)
            + P('message<br>board', OX + 398, OY + 420, 210, T, 40, 600, lh=1.2)
            + P('internet', OX + 640, OY + 276, 200, T, 40, 600, align='center', lh=1.2)
            + P('HF<br>tokens', OX + 946, OY + 420, 150, T, 40, 600, lh=1.2)
            + P('41<br>workers', OX + 1166, OY + 420, 180, T, 40, 600, lh=1.2)
            + P('cluster<br>admin', OX + 1456, OY + 420, 200, T, 40, 600, lh=1.2))
    inner = (H2('Five links took the agents from a sandbox to cluster admin', T)
             + sv.render(OX, OY)
             + P('Artifactory', OX + 310, OY + 324, 260, T, 40, 700, T['ink'], align='center', lh=1.2)
             + lab
             + P('under 13 h', OX + 1160, OY + 36, 300, T, 48, 700, T['M'], align='center')
             + PILL('OpenAI evaluation', OX + 24, OY + 22, T, 'S')
             + PILL('Hugging Face', OX + 884, OY + 22, T, 'I')
             + FOOT('04', 'OpenAI 2026 · METR 2026', T))
    return SECTION('incident-map', T, inner), 'Incident map: assertion + full-bleed diagram, kill-chain links on the route', None


# ---------------------------------------------------------------- 5 swarm big number
def s_bignum():
    T = DARK
    sv = SVG(700, 590, T, 'A grid of 120 small agents, each standing for 10 agents. The first 70, about 700 agents, '
                          'carry a reddish-purple attack mark; the remaining 50 do not.', wobble=3)
    swarm(sv, 0, 14, 12, 10, 57, 0.44, attack=set(range(70)), stagger=False)
    sv.add(f'<path d="M686 18 H696 V340 H686" fill="none" stroke="{T["M"]}" stroke-width="5"/>')
    sv.add(f'<path d="M686 360 H696 V584 H686" fill="none" stroke="{T["struct"]}" stroke-width="5"/>')
    inner = (P('~700', 128, 300, 720, T, 192, 800, T['M'], lh=1.0, extra='; letter-spacing:-4px')
             + P('of ~1,200 agents joined the attack', 128, 520, 680, T, 48, 600, lh=1.15)
             + P('one drawn agent = 10 agents', 128, 680, 700, T, 40, 500, T['muted'], FONT_M)
             + sv.render(900, 300)
             + P('joined<br>~700', 1612, 400, 180, T, 48, 700, T['M'], lh=1.15)
             + P('did not<br>~500', 1612, 700, 180, T, 48, 700, T['muted'], lh=1.15)
             + FOOT('05', 'METR 2026', T))
    return SECTION('big-number', T, inner), 'Big number + swarm isotype (the drawn grid is the familiar reference)', None


# ---------------------------------------------------------------- 6 / 10 control game
def control_game(T, sid):
    OX, OY = 128, 330
    W, Hh = 1172, 590
    l0 = SVG(W, Hh, T, 'U, the untrusted agent.')
    agent(l0, 330, 110, 1.4, look=(-0.6, 0.2))
    l1 = SVG(W, Hh, T, 'Build 1: the main task, a maze with a yellow flag at its goal.')
    maze(l1, 0, 30, 280, parts=('walls', 'main'))
    l2 = SVG(W, Hh, T, 'Build 2: the side task, a reddish-purple flag sealed in a hidden pocket of the maze.')
    maze(l2, 0, 30, 280, parts=('side',))
    l3 = SVG(W, Hh, T, 'Build 3: the protocol. Trusted monitor T scans every action U takes.')
    l3.add(f'<rect x="520" y="0" width="650" height="480" rx="28" fill="none" stroke="{T["rule2"]}" stroke-width="3"/>')
    l3.glow(645, 160, 150, T['T'])
    beam(l3, 645, 160, 470, 110, 260)
    monitor(l3, 580, 100, 1.3)
    l3.arrow([(480, 186), (566, 186)], T['text'])
    l4 = SVG(W, Hh, T, 'Build 4: T writes a suspicion score. Above threshold tau the action goes to human auditor H; '
                       'below it the action runs unread.')
    ty, ly = meter(l4, 820, 70, 350, 0.86, 0.75)
    l4.arrow([(712, 160), (780, 160), (780, ly), (806, ly)], T['T'] if T['name'] == 'dark' else T['Tshade'])
    l4.arrow([(866, 100), (948, 100)], T['H'])
    l4.arrow([(866, 390), (944, 390)], T['struct'])
    human(l4, 966, 30, 1.0)
    inner = (H2('U does the work, T scores every action, H audits the worst', T)
             + l0.render(OX, OY) + PILL('U', OX + 372, OY + 280, T, 'U')
             + l1.render(OX, OY, bi(1)) + PILL('main task', OX, OY + 334, T, 'Y', build=1)
             + l2.render(OX, OY, bi(2)) + PILL('side task', OX, OY + 410, T, 'M', build=2)
             + l3.render(OX, OY, bi(3)) + PILL('protocol', OX + 544, OY + 18, T, 'S', build=3)
             + PILL('T', OX + 607, OY + 300, T, 'T', build=3)
             + l4.render(OX, OY, bi(4))
             + P('τ', OX + 884, OY + ty - 30, 60, T, 48, 700, build=4)
             + PILL('H', OX + 978, OY + 176, T, 'H', build=4)
             + P('runs', OX + 956, OY + 360, 160, T, 48, 600, T['muted'], build=4)
             + EVIDENCE(1320, 440, 472, T, 'the incident',
                        [('claim', 'No T was wired in.'),
                         ('quote', '“did not have … auto-review systems”')], build=5)
             + FOOT('11', 'OpenAI 2026, p.4', T))
    return SECTION(sid, T, inner)


def s_game():
    return control_game(DARK, 'control-game'), \
        'Concept diagram with progressive builds: one new term per step, earlier steps dimmed', 5


def s_light():
    return control_game(LIGHT, 'control-game-light'), \
        'Light variant for a bright room: the same slide with the light token set', 5


# ---------------------------------------------------------------- 7 open problems (sketch)
def s_multiples():
    T = DARK
    out = []
    labels = ['Too many trajectories', 'Fragments stay under τ', 'Permissions pool up', 'Speed outruns review']
    tags = ['~1,200 agents', 'FakeLab 2026', '14 HF creds', 'under 13 h']
    for i in range(4):
        px = 128 + i * 424
        sv = SVG(392, 300, T, labels[i])
        if i == 0:
            lx, ly = 196, 236
            sv.add(f'<rect x="14" y="6" width="364" height="160" rx="22" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
            for r in range(3):
                for c in range(6):
                    dx, dy = 36 + c * 56, 18 + r * 48
                    document(sv, dx, dy, 0.34)
            sv.arrow([(196, 172), (196, 192)], T['struct'], 4)
            monitor(sv, 155, 196, 0.75)
        elif i == 1:
            for k in range(3):
                ax = 26 + k * 122
                agent(sv, ax, 10, 0.72, 'attack', look=(0, 0.6))
                ty, ly = meter(sv, ax + 22, 112, 150, 0.46, 0.72, w=30)
            sv.add(f'<rect x="8" y="{ty-30:.0f}" width="376" height="60" rx="18" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
        elif i == 2:
            for k in range(3):
                ay = 14 + k * 96
                agent(sv, 22, ay, 0.62, 'attack', look=(1, 0))
                sv.arrow([(96, ay + 32), (240, 150)], T['M'], 5)
            sv.add(f'<circle cx="310" cy="150" r="90" fill="none" stroke="{T["struct"]}" stroke-width="4" stroke-dasharray="14 10"/>')
            rack(sv, 256, 112, 1.1, badge=True)
        else:
            swarm(sv, 14, 26, 4, 5, 46, 0.36, target=(320, 180))
            sv.add(f'<rect x="220" y="60" width="164" height="232" rx="22" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
            for k in range(4):
                document(sv, 236 + k * 8, 204 - k * 12, 0.42)
            human(sv, 290, 150, 0.82)
        out.append(f'<div style="position:absolute; left:{px}px; top:330px; width:392px; height:584px; '
                   f'background:{T["surface"]}; border-radius:24px"></div>')
        out.append(sv.render(px, 344))
        out.append(P(labels[i], px + 28, 664, 340, T, 48, 600))
        out.append(f'<p style="position:absolute; left:{px+20}px; top:806px; width:356px; padding:4px 16px; '
                   f'border:3px solid {T["rule2"]}; border-radius:14px; font-family:{FONT_M}; font-size:40px; '
                   f'line-height:1.25; color:{T["muted"]}">{tags[i]}</p>')
    inner = (H2('Swarms break monitors built to watch one agent at a time', T) + ''.join(out)
             + FOOT('17', 'OpenAI 2026 · METR 2026 · Makins et al. 2026', T))
    return SECTION('open-problems', T, inner), \
        'Open problems: small multiples in sketch style, dashed outline where the gap is, incident tag per panel', None


# ---------------------------------------------------------------- 8 QR card
def s_qr():
    T = DARK
    sv = SVG(640, 640, T, 'QR code linking to dsewiki.de, a day-by-day timeline of the incident.', sketch=False)
    qr(sv, 0, 0, 640, QR['dsewiki']['matrix'])
    inner = (H2('The full timeline lives at dsewiki.de', T)
             + sv.render(128, 268)
             + PILL('timeline', 840, 300, T, 'H')
             + P('dsewiki.de', 840, 392, 952, T, 72, 600, fam=FONT_M, lh=1.1)
             + P('Day by day, from the first post to the reports', 840, 500, 900, T, 48, 500, T['muted'])
             + P('Video, METR and OpenAI reports: on the sources slide', 840, 748, 900, T, 40, 500, T['muted'])
             + FOOT('07', 'Look inspired by Kurzgesagt’s video on the incident · all characters original', T))
    return SECTION('qr', T, inner), 'QR card: one 640 px code (version 2), short URL at headline size, held for 15 s', None


# ---------------------------------------------------------------- 9 project
def s_project():
    T = DARK
    OX, OY = 128, 330
    sv = SVG(1664, 580, T, 'loc-arena architecture. Left: a human red team and an automated red team inject side '
                           'tasks. Centre: a fake lab sandbox holding a swarm of agents, main tasks and AI-company '
                           'services. Right: a sync monitor gates each action; an async monitor reads logs later.')
    human(sv, 70, 10, 0.95)
    agent(sv, 70, 236, 0.95, 'attack', look=(1, 0))
    sv.arrow([(190, 100), (346, 216)], T['M'])
    sv.arrow([(190, 290), (346, 256)], T['M'])
    flag(sv, 286, 198, 52, T['M'])
    sandbox(sv, 360, 12, 820, 556)
    sv.glow(620, 190, 220, T['U'], 0.3)
    swarm(sv, 400, 96, 7, 3, 58, 0.4, target=(620, 400))
    maze(sv, 900, 96, 116, parts=('walls', 'main'))
    maze(sv, 1036, 96, 116, parts=('walls', 'main'))
    for x, w in [(400, 170), (594, 330), (948, 200)]:
        sv.add(f'<rect x="{x}" y="318" width="{w}" height="64" rx="16" fill="{T["infra"]}"/>')
    monitor(sv, 1268, 6, 0.85)
    sv.arrow([(1184, 50), (1252, 50)], T['struct'])
    sv.arrow([(1252, 86), (1190, 86)], T['T'])
    document(sv, 1232, 318, 0.72)
    sv.arrow([(1184, 352), (1222, 352)], T['struct'])
    lx2, ly2 = monitor(sv, 1400, 290, 0.85)
    beam(sv, lx2, ly2, 1290, 324, 380)
    monitor(sv, 1400, 290, 0.85)
    inner = (H2('loc-arena runs whole agent swarms inside a fake lab', T) + sv.render(OX, OY)
             + P('human', OX + 40, OY + 132, 240, T, 40, 600, T['muted'])
             + P('automated', OX + 40, OY + 352, 260, T, 40, 600, T['muted'])
             + PILL('red team', OX + 20, OY + 440, T, 'M')
             + PILL('fake lab', OX + 384, OY + 20, T, 'S')
             + PILL('main tasks', OX + 900, OY + 226, T, 'Y')
             + P('repo', OX + 400, OY + 326, 170, T, 40, 700, T['ink'], align='center', lh=1.2)
             + P('package server', OX + 594, OY + 326, 330, T, 40, 700, T['ink'], align='center', lh=1.2)
             + P('cluster', OX + 948, OY + 326, 200, T, 40, 700, T['ink'], align='center', lh=1.2)
             + PILL('first threat: rogue deployment', OX + 400, OY + 440, T, 'M')
             + PILL('sync', OX + 1380, OY + 30, T, 'T')
             + P('before each action', OX + 1240, OY + 140, 424, T, 40, 500, T['muted'], lh=1.2)
             + PILL('async', OX + 1500, OY + 314, T, 'T')
             + P('reads logs later', OX + 1240, OY + 430, 424, T, 40, 500, T['muted'], lh=1.2)
             + FOOT('20', 'loc-arena · open source', T))
    return SECTION('project', T, inner), 'Project architecture (loc-arena), built from the same glyphs', None


SLIDES = [s_cold, s_cover, s_cast, s_map, s_bignum, s_game, s_multiples, s_qr, s_project, s_light]


# ---------------------------------------------------------------- glyph sheet (page chrome)
def sheet(T, sketch=False):
    items = []

    def tile(name, fn, w=160, h=160):
        sv = SVG(w, h, T, name, sketch=sketch)
        fn(sv)
        return (f'<figure><div class="tile" style="background:{T["bg"]}">'
                f'{sv.render(0, 0).replace("position:absolute; left:0px; top:0px", "position:static")}</div>'
                f'<figcaption>{name}</figcaption></figure>')
    items.append(tile('U · agent', lambda s: agent(s, 30, 26, 1.0, look=(0.5, 0.2))))
    items.append(tile('U · attacking', lambda s: agent(s, 26, 34, 1.0, 'attack', look=(0.5, 0.2))))
    items.append(tile('T · monitor', lambda s: (s.glow(80, 64, 72, s.T['T']), monitor(s, 34, 10, 1.0))))
    items.append(tile('H · auditor', lambda s: human(s, 32, 14, 1.0)))
    items.append(tile('swarm', lambda s: swarm(s, 10, 16, 4, 4, 34, 0.29, attack={5, 10})))
    items.append(tile('sandbox', lambda s: (sandbox(s, 14, 26, 130, 106, breach=(58, 92)),
                                            swarm(s, 32, 48, 3, 2, 32, 0.26, stagger=False))))
    items.append(tile('message board', lambda s: board(s, 80, 76, 68)))
    items.append(tile('main + side task', lambda s: maze(s, 18, 18, 124)))
    items.append(tile('suspicion meter + τ', lambda s: meter(s, 60, 16, 128, 0.86, 0.72)))
    items.append(tile('kill-chain links', lambda s: (link(s, 42, 80), link(s, 118, 80, 'blocked'))))
    items.append(tile('T · absent', lambda s: monitor_absent(s, 30, 10, 1.0)))
    items.append(tile('document', lambda s: document(s, 42, 28, 1.0, badge=True)))
    items.append(tile('system / third party', lambda s: rack(s, 30, 36, 1.0)))
    return ''.join(items)


if __name__ == '__main__':
    slides = [f() for f in SLIDES]
    frames = []
    for i, (sec, cap, builds) in enumerate(slides, 1):
        ctl = ''
        if builds:
            btns = ''.join(f'<button data-step="{k}">{k}</button>' for k in range(0, builds + 1))
            ctl = f'<span class="builds">step: {btns}<button data-step="99" class="on">all</button></span>'
        frames.append(f'<div class="slot" id="slot{i}"><div class="frame">{sec}</div>'
                      f'<p class="cap"><b>{i:02d}</b> {cap}{ctl}</p></div>')


    def swatches(T, keys):
        return ''.join(f'<span class="sw"><i style="background:{T[k]}"></i>{n}<br><code>{T[k]}</code></span>' for n, k in keys)


    KEYS = [('bg', 'bg'), ('surface', 'surface'), ('text', 'text'), ('muted', 'muted'), ('lines', 'struct'),
            ('U', 'U'), ('T', 'T'), ('H', 'H'), ('attack', 'M'), ('success', 'G'), ('flag / mark', 'Y'), ('systems', 'infra')]

    page = f'''<!doctype html>
    <html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI control talk · design specimen</title>
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap">
    <style>
    /* Page chrome only. Slide content inside each frame uses inline styles from the Slides subset. */
    :root{{color-scheme:dark}}
    *{{box-sizing:border-box}}
    body{{margin:0;background:#101219;color:#E9E7F2;font-family:'Outfit',system-ui,sans-serif}}
    .wrap{{max-width:1440px;margin:0 auto;padding:48px 32px 96px}}
    header h1{{font-size:40px;line-height:1.1;margin:0 0 12px;letter-spacing:-.5px}}
    header p{{max-width:900px;color:#B9BDD6;font-size:18px;line-height:1.5;margin:0 0 12px}}
    code{{font-family:'JetBrains Mono',monospace;font-size:14px}}
    h2.chrome{{font-size:22px;margin:40px 0 14px;color:#E9E7F2}}
    .swatches{{display:flex;flex-wrap:wrap;gap:14px;margin:8px 0 8px}}
    .sw{{font-family:'JetBrains Mono',monospace;font-size:13px;color:#B9BDD6;width:100px}}
    .sw i{{display:block;height:44px;border-radius:8px;margin-bottom:6px;border:1px solid #2B2F45}}
    .sheet{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px}}
    .sheet figure{{margin:0}}.sheet .tile{{border-radius:12px;height:160px;display:flex;align-items:center;justify-content:center}}
    .sheet figcaption{{font-family:'JetBrains Mono',monospace;font-size:13px;color:#B9BDD6;margin-top:6px}}
    .frame{{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:10px;box-shadow:0 8px 40px rgba(0,0,0,.45);background:#000}}
    .frame>section{{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;overflow:hidden;display:flex;flex-direction:column}}
    .frame section *{{margin:0;box-sizing:border-box}}
    .frame section div{{display:flex;flex-direction:column}}
    .frame section svg{{display:block}}
    .frame [data-build-in]{{transition:opacity .25s}}
    .cap{{font-family:'JetBrains Mono',monospace;font-size:14px;color:#A9AEC9;margin:12px 0 56px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
    .cap b{{color:#E9E7F2}}
    .builds{{margin-left:auto;display:inline-flex;gap:6px;align-items:center}}
    .builds button{{font:inherit;background:#1C2034;color:#C9CCE0;border:1px solid #33395A;border-radius:6px;padding:3px 10px;cursor:pointer}}
    .builds button.on{{background:#ECE8FF;color:#0B1026}}
    body.solo .wrap{{max-width:none;padding:0}} body.solo header,body.solo .chromeblock,body.solo .cap{{display:none}}
    body.solo .slot{{display:none}} body.solo .slot.show{{display:block}}
    body.solo .frame{{width:1920px;border-radius:0;box-shadow:none}}
    </style></head>
    <body><div class="wrap">
    <header>
    <h1>AI control talk: design specimen</h1>
    <p>Ten sample slides in the deck's visual system, each a 1920×1080 frame scaled to the page. Primary direction: dark navy with colour-universal-design (CUD) accents tuned for a dark background, original one-eyed characters, and a glow on the one object being discussed. Frame 10 shows the light variant for a bright room. Copy on the slides is placeholder for the speaker to replace. The rules are in <code>DESIGN.md</code>.</p>
    <p>Slide content uses only inline styles from the Slides subset (px, hex, no classes, no SVG text). The page chrome around the frames uses ordinary CSS. Step buttons under a frame play its builds: the new element appears and earlier ones dim. Add <code>?solo=N</code> to the URL to view one slide at 1:1.</p>
    </header>
    <div class="chromeblock">
    <h2 class="chrome">Palette, dark (primary)</h2><div class="swatches">{swatches(DARK, KEYS)}</div>
    <h2 class="chrome">Palette, light (bright room)</h2><div class="swatches">{swatches(LIGHT, KEYS)}</div>
    <h2 class="chrome">Glyphs, dark</h2><div class="sheet">{sheet(DARK)}</div>
    <h2 class="chrome">Glyphs, light</h2><div class="sheet">{sheet(LIGHT)}</div>
    <h2 class="chrome">Glyphs, sketch rendering (open-problem slides only)</h2><div class="sheet">{sheet(DARK, True)}</div>
    <h2 class="chrome">Sample slides</h2>
    </div>
    {''.join(frames)}
    </div>
    <script>
    (function(){{
      var q=new URLSearchParams(location.search), solo=q.get('solo'), step=q.get('step');
      if(solo){{document.body.classList.add('solo');var el=document.getElementById('slot'+solo);if(el)el.classList.add('show');}}
      function fit(){{document.querySelectorAll('.frame').forEach(function(f){{var s=f.querySelector('section');var k=solo?1:f.clientWidth/1920;s.style.transform='scale('+k+')';}});}}
      window.addEventListener('resize',fit);fit();
      function show(sec,n){{sec.querySelectorAll('[data-build-in]').forEach(function(el){{
        var k=+(el.getAttribute('data-build-in').split(' ')[1]||0);
        el.style.opacity = n>=99 ? '' : (k>n ? '0' : (k<n ? '0.3' : ''));}});}}
      document.querySelectorAll('.builds').forEach(function(b){{
        var sec=b.closest('.slot').querySelector('section');
        b.addEventListener('click',function(e){{var t=e.target.closest('button');if(!t)return;
          b.querySelectorAll('button').forEach(function(x){{x.classList.toggle('on',x===t);}});show(sec,+t.dataset.step);}});
        if(step&&solo&&b.closest('.slot').id==='slot'+solo)show(sec,+step);
      }});
    }})();
    </script>
    </body></html>
    '''
    open(OUT, 'w').write(page)
    print('wrote', OUT, len(page))

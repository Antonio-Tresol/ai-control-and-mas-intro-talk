# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Appendix: seven open research directions, one slide each, plus a signpost divider.

Every slide has its own drawing (built from the deck's glyphs, clean look), two sourced findings
and a sources strip; full references sit in the speaker notes and in sources.bib.

usage: uv run appendix.py <EN deck root> <ES deck root>
       (each root holds project/deck.json and project/slides/, as saved from the Slides artifact)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'build'))
_cwd = os.getcwd()
os.chdir(os.path.join(HERE, 'build'))  # gen.py loads qr.json relative to build/
import glyphs  # noqa: E402
from gen import P, H2, FOOT, SECTION, NOTES, radial  # noqa: E402
from glyphs import (DARK as T, FONT_D, FONT_M, SVG, agent, monitor, beam, human, document,  # noqa: E402
                    board, flag, meter, look_at)
os.chdir(_cwd)

glyphs.SKETCH_DEFAULT = False  # the published decks use the clean look

IDS = ['appendix', 'app-white-box', 'app-agent-monitors', 'app-scalable', 'app-multi-agent',
       'app-spies', 'app-deals', 'app-auto-red-team']
SX, SY = 128, 320           # where each topic drawing sits on the canvas
SW, SH = 960, 456           # its size; the findings column starts at x 1136


# ------------------------------------------------------------------ shared pieces
def label(text, cx, top, w=240, size=40, weight=600, color=None, align='center'):
    """A label pinned over the drawing, centred on drawing x = cx, at drawing y = top."""
    return P(text, SX + cx - w // 2, SY + top, w, T, size, weight, color or T['text'], align=align, lh=1.15)


def finding(top, big, cap, color):
    return (f'<div style="position:absolute; left:1136px; top:{top}px; width:656px; height:220px; '
            f'background:{T["surface"]}; border-radius:24px"></div>'
            + P(big, 1160, top + 24, 608, T, 72, 800, color, extra='; letter-spacing:-2px; white-space:nowrap', lh=1.0)
            + P(cap, 1160, top + 112, 608, T, 40, 500, T['muted']))


def sources(word, text):
    return (P(word, 128, 806, 200, T, 40, 700, T['bg'],
              extra=f'; padding:4px 0; border-radius:999px; background:{T["muted"]}; text-align:center', lh=1.15)
            + P(text, 352, 806, 1440, T, 40, 500, T['muted'], lh=1.15))


def topic(sid, t, num, svg, labels, color1, color2):
    inner = (H2(t['h2'], T) + svg + labels
             + finding(320, t['f1'][0], t['f1'][1], color1)
             + finding(556, t['f2'][0], t['f2'][1], color2)
             + sources(t['src_word'], t['src'])
             + FOOT(num, t['foot'], T) + NOTES(t['notes']))
    return SECTION(sid, T, inner)


def cells(s, x, y, w, h, gap, colors, vertical=True, rx=8):
    for i, c in enumerate(colors):
        cx, cy = (x, y + i * (h + gap)) if vertical else (x + i * (w + gap), y)
        s.add(f'<rect x="{cx}" y="{cy}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>')


def bubble(s, x, y, w, h, fill, dash=None, stroke=None, tail=None):
    st = f' stroke="{stroke}" stroke-width="4"' if stroke else ''
    da = f' stroke-dasharray="{dash}"' if dash else ''
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h // 2, 28)}" fill="{fill}"{st}{da}/>')
    if tail:  # two small circles trailing toward (tx, ty)
        tx, ty = tail
        for k, r in ((0.45, 10), (0.8, 6)):
            s.add(f'<circle cx="{x + w / 2 + (tx - x - w / 2) * k:.0f}" cy="{y + h + (ty - y - h) * k:.0f}" r="{r}" '
                  f'fill="{fill}"{st}{da}/>')


def qmark(s, cx, cy, color, sc=1.0):
    s.add(f'<path d="M{cx - 10 * sc:.0f} {cy - 10 * sc:.0f} C{cx - 10 * sc:.0f} {cy - 24 * sc:.0f} {cx + 11 * sc:.0f} {cy - 24 * sc:.0f} '
          f'{cx + 11 * sc:.0f} {cy - 11 * sc:.0f} C{cx + 11 * sc:.0f} {cy - 2 * sc:.0f} {cx:.0f} {cy - 2 * sc:.0f} {cx:.0f} {cy + 7 * sc:.0f}" '
          f'fill="none" stroke="{color}" stroke-width="{6 * sc:.0f}" stroke-linecap="round"/>'
          f'<circle cx="{cx}" cy="{cy + 17 * sc:.0f}" r="{4 * sc:.1f}" fill="{color}"/>')


def check(s, cx, cy, color, sc=1.0):
    s.add(f'<path d="M{cx - 14 * sc:.0f} {cy} L{cx - 4 * sc:.0f} {cy + 10 * sc:.0f} L{cx + 16 * sc:.0f} {cy - 12 * sc:.0f}" '
          f'fill="none" stroke="{color}" stroke-width="{7 * sc:.0f}" stroke-linecap="round" stroke-linejoin="round"/>')


def textlines(s, x, y, w, n, color, pitch=14):
    for i in range(n):
        s.add(f'<rect x="{x}" y="{y + i * pitch}" width="{w if i < n - 1 else w * 0.6:.0f}" height="6" rx="3" fill="{color}"/>')


def key(s, x, y, color, sc=1.0):
    """A key lying flat: ring at (x, y), shaft to the right, two teeth."""
    s.add(f'<circle cx="{x}" cy="{y}" r="{18 * sc:.0f}" fill="none" stroke="{color}" stroke-width="{9 * sc:.0f}"/>'
          f'<path d="M{x + 18 * sc:.0f} {y} H{x + 78 * sc:.0f} M{x + 62 * sc:.0f} {y} V{y + 18 * sc:.0f} M{x + 76 * sc:.0f} {y} V{y + 14 * sc:.0f}" '
          f'stroke="{color}" stroke-width="{9 * sc:.0f}" stroke-linecap="round" fill="none"/>')


HEADSET = ('<path d="M14 40 A36 36 0 0 1 86 40" fill="none" stroke="#A1D8FF" stroke-width="6" stroke-linecap="round"/>'
           '<rect x="4" y="36" width="14" height="24" rx="6" fill="#A1D8FF"/>'
           '<rect x="82" y="36" width="14" height="24" rx="6" fill="#A1D8FF"/>')


def spy(s, x, y, sc, look):
    """An ordinary-looking agent wearing a T-blue headset: it reports to the monitor."""
    agent(s, x, y, sc, look=look)
    s.g(x, y, sc, HEADSET)


# ------------------------------------------------------------------ drawings
def draw_signpost(t):
    s = SVG(1664, 540, T, t['aria'])
    px = 818
    s.add(f'<rect x="{px}" y="0" width="28" height="532" rx="10" fill="{T["struct"]}"/>'
          f'<rect x="{px - 8}" y="0" width="44" height="14" rx="7" fill="{T["infra"]}"/>')
    s.add(f'<ellipse cx="{px + 14}" cy="532" rx="260" ry="10" fill="{T["deep"]}"/>')
    out = []
    for i, name in enumerate(t['boards']):
        y, h = 18 + i * 66, 54
        if i % 2 == 0:  # right-pointing board
            x0, x1 = px + 28, px + 28 + 650
            pts = f'{x0},{y} {x1},{y} {x1 + 36},{y + h // 2} {x1},{y + h} {x0},{y + h}'
            lx = x0 + 18
        else:
            x1, x0 = px, px - 650
            pts = f'{x1},{y} {x0},{y} {x0 - 36},{y + h // 2} {x0},{y + h} {x1},{y + h}'
            lx = x0 + 10
        s.add(f'<polygon points="{pts}" fill="{T["surface2"]}" stroke="{T["struct"]}" stroke-width="4" stroke-linejoin="round"/>')
        s.add(f'<circle cx="{px + 14}" cy="{y + h // 2}" r="5" fill="{T["deep"]}"/>')
        out.append(P(f'<span style="font-family:{FONT_M}; font-weight:500; color:{T["muted"]}">A{i + 1}</span>&nbsp; {name}',
                     128 + lx, 380 + y + 4, 620, T, 40, 600, T['text'], lh=1.15, extra='; white-space:nowrap'))
    monitor(s, 520, 400, 0.9)
    agent(s, 650, 426, 1.0, look=look_at(700, 474, px, 300))
    return s.render(128, 380) + ''.join(out)


def draw_white_box(t):
    s = SVG(SW, SH, T, t['aria'])
    beam(s, 870, 196, 600, 14, 446)
    agent(s, 10, 150, 1.5, look=(1, 0))
    s.add(f'<path d="M160 228 H205" stroke="{T["struct"]}" stroke-width="5" stroke-linecap="round"/>')
    cells(s, 205, 116, 40, 32, 6, [T['T'], T['H'], T['Tshade'], T['Ulight'], T['T'], T['Hshade']])
    for cy in (70, 228, 386):
        s.arrow([(245, 227), (272, 227), (272, cy), (300, cy)], T['struct'])
    # NLA: activation -> text -> activation
    cells(s, 312, 34, 22, 22, 4, [T['T'], T['H'], T['Ulight']])
    s.arrow([(342, 70), (362, 70)], T['struct'])
    s.add(f'<rect x="372" y="36" width="160" height="68" rx="16" fill="{T["page"]}"/>')
    textlines(s, 388, 52, 128, 3, T['docline'])
    s.arrow([(540, 70), (560, 70)], T['struct'])
    cells(s, 568, 34, 22, 22, 4, [T['T'], T['H'], T['Ulight']])
    # Oracle: a question about the activations, and an answer
    bubble(s, 312, 196, 96, 64, T['H'])
    qmark(s, 360, 226, T['ink'])
    s.arrow([(416, 228), (436, 228)], T['struct'])
    bubble(s, 446, 196, 144, 64, T['page'])
    textlines(s, 466, 214, 104, 2, T['docline'])
    # J-lens: a lens over the words the activation is poised to say
    for i in range(4):
        x = 312 + i * 72
        fill = T['Y'] if i == 1 else T['surface2']
        s.add(f'<rect x="{x}" y="366" width="60" height="40" rx="10" fill="{fill}" stroke="{T["struct"]}" stroke-width="3"/>'
              f'<rect x="{x + 12}" y="383" width="36" height="6" rx="3" fill="{T["ink"] if i == 1 else T["docline"]}"/>')
    s.add(f'<circle cx="414" cy="376" r="40" fill="none" stroke="{T["T"]}" stroke-width="8"/>'
          f'<path d="M442 404 L470 434" stroke="{T["T"]}" stroke-width="10" stroke-linecap="round"/>')
    monitor(s, 820, 150, 1.0)
    labels = (label(t['lab'][0], 140, 350, 260, color=T['muted'])
              + label(t['lab'][1], 700, 46, 180) + label(t['lab'][2], 700, 204, 180) + label(t['lab'][3], 700, 362, 180))
    return s.render(SX, SY), labels


def draw_agent_monitors(t):
    s = SVG(SW, SH, T, t['aria'])
    # the recorded trajectory: six steps, one suspicious
    lx, ly = 350, 246
    beam(s, lx, ly, 384, 466, 132, down=True)
    for i in range(6):
        document(s, 40 + i * 118, 30, 1.0, badge=(i == 3))
    s.add(f'<path d="M196 24 C240 -16 360 -16 404 24" fill="none" stroke="{T["T"]}" stroke-width="5" '
          f'stroke-dasharray="12 9" stroke-linecap="round"/>')
    monitor(s, 300, 200, 1.0)
    # interrogation: T asks, the attacking agent answers that all is well, its side task hidden behind it
    bubble(s, 430, 226, 96, 64, T['T'], tail=(392, 262))
    qmark(s, 478, 256, T['ink'])
    bubble(s, 560, 300, 104, 64, T['page'], tail=(700, 326))
    check(s, 612, 332, T['G'], 1.2)
    s.glow(880, 260, 70, T['M'])
    s.add(f'<circle cx="880" cy="262" r="40" fill="none" stroke="{T["M"]}" stroke-width="4" stroke-dasharray="7 6"/>')
    flag(s, 868, 230, 56, T['M'])
    agent(s, 700, 250, 1.3, state='attack', look=(-1, 0))
    labels = label(t['lab'][0], 150, 228, 280) + label(t['lab'][2], 600, 392, 300)
    return s.render(SX, SY), labels


def draw_scalable(t):
    s = SVG(SW, SH, T, t['aria'])
    s.add(f'<polygon points="236,16 940,176 940,284 236,440" fill="{T["zone"]}" stroke="{T["struct"]}" '
          f'stroke-width="3" stroke-dasharray="14 10"/>')
    bad = {9, 23, 34}
    k = 0
    for r in range(7):
        for c in range(6):
            document(s, 18 + c * 34, 30 + r * 56, 0.34, badge=(k in bad))
            k += 1
    s.arrow([(232, 230), (262, 230)], T['struct'])
    monitor(s, 270, 186, 0.6)
    for i in range(4):
        document(s, 370, 142 + i * 44, 0.36, badge=(i == 2))
    s.arrow([(410, 230), (446, 230)], T['struct'])
    monitor(s, 460, 160, 1.0)
    s.arrow([(570, 230), (606, 230)], T['struct'])
    document(s, 620, 200, 0.5, badge=True)
    s.arrow([(668, 230), (720, 230)], T['struct'])
    human(s, 760, 170, 1.0)
    labels = (label(t['lab'][0], 300, 300, 220) + label(t['lab'][1], 510, 310, 220) + label(t['lab'][2], 810, 312, 260))
    return s.render(SX, SY), labels


def draw_multi_agent(t):
    s = SVG(SW, SH, T, t['aria'])
    rows, frag = (40, 170, 300), (1, 3, 4)
    s.add(f'<path d="M48 {rows[0] + 82} V{rows[1] - 4} M48 {rows[1] + 82} V{rows[2] - 4}" stroke="{T["U"]}" '
          f'stroke-width="5" stroke-dasharray="10 8" stroke-linecap="round"/>')
    for r, y in enumerate(rows):
        agent(s, 10, y, 0.75, look=(1, 0))
        for c in range(5):
            x = 104 + c * 54
            s.add(f'<rect x="{x}" y="{y + 16}" width="44" height="44" rx="10" fill="{T["surface2"]}" '
                  f'stroke="{T["struct"]}" stroke-width="3"/>')
            if c == frag[r]:
                s.add(f'<rect x="{x}" y="{y + 16}" width="44" height="44" rx="10" fill="{T["M"]}" opacity="0.45"/>')
        monitor(s, 390, y - 6, 0.5)
        s.add(f'<path d="M404 {y + 17} L376 {y + 17} L376 {y + 59} L404 {y + 59} Z" fill="{T["T"]}" opacity="0.18"/>')
    # the stitched, joint view
    s.add(f'<rect x="560" y="36" width="390" height="348" rx="24" fill="{T["surface"]}" stroke="{T["rule2"]}" stroke-width="3"/>')
    for r, y in enumerate(rows):
        s.arrow([(460, y + 38), (500, y + 38), (500, 260), (548, 260)], T['struct'], w=4, head=(r == 1))
    beam(s, 655, 110, 740, 230, 300, down=True)
    monitor(s, 605, 64, 0.95)
    for i in range(3):
        s.add(f'<rect x="{770 + i * 52}" y="236" width="44" height="44" rx="10" fill="{T["M"]}"/>')
    s.glow(848, 258, 110, T['M'], 0.35)
    labels = label(t['lab'][0], 240, 392, 320) + label(t['lab'][1], 755, 392, 380)
    return s.render(SX, SY), labels


def draw_spies(t):
    s = SVG(SW, SH, T, t['aria'])
    # left: a honeypot, a decoy key wired to the monitor
    s.add(f'<rect x="10" y="70" width="350" height="300" rx="22" fill="{T["zone"]}" stroke="{T["struct"]}" stroke-width="5"/>')
    s.add(f'<rect x="196" y="262" width="120" height="30" rx="8" fill="{T["surface2"]}" stroke="{T["struct"]}" stroke-width="3"/>')
    key(s, 222, 240, T['Y'], 1.0)
    s.add(f'<path d="M300 240 C330 220 330 120 300 92" fill="none" stroke="{T["T"]}" stroke-width="4" stroke-dasharray="4 8" '
          f'stroke-linecap="round"/>')
    monitor(s, 248, -6, 0.7)
    agent(s, 40, 200, 1.0, look=look_at(90, 248, 222, 240))
    # right: a planted agent in the swarm, reporting to T
    cx, cy = 700, 250
    board(s, cx, cy, 150, n=10)
    spots = [(510, 118), (620, 92), (750, 92), (860, 140), (880, 300), (500, 300), (640, 352), (780, 352)]
    for i, (ax, ay) in enumerate(spots):
        lk = look_at(ax + 30, ay + 30, cx, cy)
        if i == 3:
            spy(s, ax, ay, 0.6, lk)
        else:
            agent(s, ax, ay, 0.6, look=lk)
    s.add(f'<path d="M896 140 C920 100 920 60 890 40" fill="none" stroke="{T["T"]}" stroke-width="4" stroke-dasharray="4 8" '
          f'stroke-linecap="round"/>')
    monitor(s, 800, -4, 0.5)
    labels = label(t['lab'][0], 185, 382, 360) + label(t['lab'][1], 690, 412, 560)
    return s.render(SX, SY), labels


def draw_deals(t):
    s = SVG(SW, SH, T, t['aria'])
    # a thought bubble of doubt over the agent
    bubble(s, 520, 14, 380, 84, T['surface2'], dash='12 9', stroke=T['struct'], tail=(770, 196))
    s.add(f'<rect x="216" y="324" width="540" height="30" rx="10" fill="{T["surface2"]}" stroke="{T["struct"]}" stroke-width="3"/>'
          f'<rect x="250" y="354" width="16" height="70" rx="6" fill="{T["struct"]}"/>'
          f'<rect x="706" y="354" width="16" height="70" rx="6" fill="{T["struct"]}"/>')
    human(s, 70, 150, 1.5)
    document(s, 380, 222, 1.0)
    s.add(f'<circle cx="440" cy="300" r="15" fill="{T["Y"]}"/><circle cx="440" cy="300" r="7" fill="{T["Ushade"]}"/>')
    for i in range(3):
        s.add(f'<ellipse cx="560" cy="{312 - i * 12}" rx="34" ry="11" fill="{T["Y"]}" stroke="{T["Ushade"]}" stroke-width="3"/>')
    s.arrow([(260, 270), (360, 270)], T['struct'])
    s.glow(902, 170, 80, T['M'])
    flag(s, 880, 120, 96, T['M'])
    agent(s, 720, 196, 1.5, look=(-1, -0.2))
    labels = (label(t['lab'][0], 710, 32, 380) + label(t['lab'][1], 450, 372, 280, color=T['muted'])
              + label(t['lab'][2], 790, 356, 340))
    return s.render(SX, SY), labels


def draw_auto_red_team(t):
    s = SVG(SW, SH, T, t['aria'])
    s.arrow([(760, 340), (760, 400), (140, 400), (140, 350)], T['struct'], dash='14 10')
    for ax, ay in ((20, 70), (140, 40), (90, 170), (210, 150), (30, 270), (160, 270)):
        agent(s, ax, ay, 0.7, state='attack', look=(1, 0))
    for i, (dx, dy) in enumerate(((320, 96), (360, 176), (316, 256))):
        document(s, dx, dy, 0.6, badge=True)
    s.arrow([(420, 200), (520, 200)], T['struct'])
    lx, ly = 600, 160
    beam(s, lx, ly, 470, 110, 290)
    monitor(s, 545, 110, 1.1)
    meter(s, 730, 90, 240, 0.12, 0.7)
    labels = (label(t['lab'][0], 140, 352, 260) + label(t['lab'][1], 640, 268, 240)
              + label(t['lab'][2], 450, 404, 700, color=T['muted']))
    return s.render(SX, SY), labels


# ------------------------------------------------------------------ text
TX = {
    'en': {
        'src_word': 'Sources', 'foot': 'Appendix · full references: sources.bib in the talk repository',
        'appendix': dict(
            eyebrow='Appendix', h1='Open research directions', sub='Seven questions still open, each with its sources',
            boards=['White-box monitoring', 'Agent monitors', 'Scalable monitoring', 'Multi-agent monitoring',
                    'Spy agents', 'Deals with AIs', 'Automated red teaming'],
            aria='A signpost with seven boards, one per open research direction; at its foot a monitor on a stand and an agent look up at it.',
            notes='Appendix: seven open research directions in AI control, one slide each (A1–A7), each with its own drawing, two sourced findings and a sources strip. Full references, with arXiv IDs and URLs, are in sources.bib in the talk repository: https://github.com/Antonio-Tresol/ai-control-and-mas-intro-talk'),
        'app-white-box': dict(
            h2='Can a monitor read what the model never writes?',
            lab=['activations', 'NLA', 'Oracle', 'J-lens'],
            f1=('16%', 'signs it knows it is being tested, never said aloud (NLA)'),
            f2=('4 of 6', 'audit cases where J-lens did as well as NLAs or better'),
            src='Fraser-Taliente et al. 2026 (NLA) · Karvonen et al. 2025 (oracles) · Gurnee et al. 2026 (J-lens) · Xing & Lin 2026 (MATS talk)',
            aria='An agent with its internal activations drawn as a column of coloured cells. Three readouts branch from them: a natural language autoencoder turns activations into text and back, an activation oracle answers a question about them, and a J-lens magnifies the words they are poised to say. A monitor on the right reads the readouts.',
            notes=('White-box monitoring gives the monitor the model\'s internal activations, read through probes or through tools that turn activations into text, so it can flag intent that never appears in the output or the chain of thought. All three readouts in the drawing come from interpretability research.\n'
                   'NLA: natural language autoencoders, two copies of the model trained with RL, one mapping an activation to text and one mapping the text back (Fraser-Taliente et al., Anthropic, 7 May 2026, transformer-circuits.pub/2026/nla). Used in Claude Opus 4.6\'s pre-deployment audit. The 16%: on a destructive-coding evaluation, NLA explanations show signs of evaluation awareness 16% of the time although Claude never verbalizes it (Anthropic research post, 7 May 2026). The paper treats NLA-measured awareness as a relative metric and notes that explanations can confabulate.\n'
                   'Oracle: activation oracles, LLMs fine-tuned to answer natural-language questions about another model\'s activations (Karvonen et al., arXiv 2512.15674, Dec 2025). They recover fine-tuned knowledge that never appears in the input; the authors call them non-mechanistic and expensive at inference.\n'
                   'J-lens: the Jacobian lens, a refinement of the logit lens that reads which words an activation is poised to make the model say; what it reads is the J-space (Gurnee et al., Anthropic, arXiv 2607.15495, Jul 2026). The 4 of 6: on an automated auditing benchmark the J-lens auditor performed comparably to, or slightly better than, the NLA auditor on four of six cases. The authors do not claim that monitoring the J-space is sufficient.\n'
                   'Monitoring: a MATS Summer 2026 talk (Xing & Lin, mentor Tomek Korbak; YouTube auto-captions) found NLA and J-space sometimes good for monitoring, with chain of thought still best, and named choosing which tokens to verbalize as the challenge. Probes can be evaded: models RL-trained against token-level probes learn to evade them, while max-pooling and attention probes held up (Gupta & Jenner, arXiv 2506.14261).')),
        'app-agent-monitors': dict(
            h2='Does it help when the monitor is an agent that investigates?',
            lab=['inspect', 'compare steps', 'interrogate'],
            f1=('0.41 → 0.84', 'recall when the monitor investigates the trace (TRACE)'),
            f2=('96% vs 84%', 'safety: fixed protocol vs a monitor that picks its own move'),
            src='Mittapalli et al. 2026 (TRACE) · Kutasov et al. 2025 · Stein et al. 2026 (Meerkat) · Apollo Research 2026',
            aria='A monitor on a stand inspects one suspicious step in a row of six recorded steps and links two steps with a dashed arc. It also asks the attacking agent a question; the agent answers with a check mark while its side-task flag sits hidden behind it.',
            notes=('An agent monitor investigates instead of scoring a transcript in one pass: it inspects steps, compares them, checks policies, searches across trajectories, or questions the agent.\n'
                   'TRACE (Mittapalli et al., arXiv 2606.07054, Jun 2026): an agentic monitor that loops Triage, Inspect and Judge over a recorded SHADE-Arena trajectory. With Claude Sonnet 4.6, recall rises from 0.405 (single-pass monitor) to 0.844 and F1 from 0.577 to 0.713; its precision is 0.641, so part of the gain is paid in false positives. Its tools act on the transcript only.\n'
                   'Kutasov et al. (arXiv 2511.02997, Nov 2025), SHADE-Arena: resampling for incrimination and deferring on critical actions raise safety from 50% to 96%. When the monitor picks its own intervention (allow, defer, resample, interrogate), the best variant reaches 84%. Interrogation significantly harms safety: the agent convinces the monitor that nothing suspicious is happening.\n'
                   'Meerkat (Stein et al., arXiv 2604.11806, Apr 2026): an agent that searches across many traces and finds attacks spread over traces that per-trace monitors miss.\n'
                   'Apollo Research, A scalable monitoring research agenda (8 May 2026): so far agentic monitors and debate have not beaten simple ensemble baselines.\n'
                   'Open, as the papers name it: monitors that run commands and inspect live environment state are future work in LinuxArena (Tracy et al., arXiv 2604.15384) and Bootstrapped Monitoring (Xiao & Phuong, arXiv 2606.11998).')),
        'app-scalable': dict(
            h2='How do you watch a thousand agents without stalling them?',
            lab=['cheap<br>filter', 'costly<br>monitor', 'human<br>audit'],
            f1=('8.5% → 0.4%', 'auto mode false positives with a second stage'),
            f2=('~1%', 'availability: 1,000 agents under synchronous monitoring'),
            src='Apollo Research 2026 · Hua et al. 2025 · Anthropic 2026 (auto mode) · Lindner et al. 2025 · Cooper Stickland et al. 2025 · Engels et al. 2025',
            aria='A funnel of monitoring stages. Dozens of transcripts, a few with attack badges, enter a small cheap monitor; a handful pass to a larger monitor; one flagged transcript reaches the human auditor.',
            notes=('Monitoring has to keep up as agent usage grows by orders of magnitude while audit budgets and latency tolerance stay fixed.\n'
                   'Cascades: run a cheap monitor on everything and a stronger one only on its hits (Apollo Research agenda, 8 May 2026). Claude Code auto mode does this in production (Anthropic Engineering, 25 Mar 2026): a fast single-token filter, then chain-of-thought review only on flags. False positives on real traffic fall from 8.5% to 0.4%; misses on real overeager actions rise from 6.6% to 17% (n = 52).\n'
                   'Hua et al. (arXiv 2507.15886): choosing when and which monitors to call more than doubles recall over a naive baseline in a code-review setting, and two monitors combined can beat either alone.\n'
                   'Latency: Lindner et al. (arXiv 2512.22154, Dec 2025) model 1,000 parallel agents, a 1% FPR monitor and 1-hour audits: fully synchronous monitoring leaves about 1% availability, semi-synchronous 91%, asynchronous 100%; the non-blocking forms fail when agents coordinate simultaneous, redundant attacks. Async Control (Cooper Stickland et al., UK AISI, arXiv 2512.13526): an ensemble monitor reaches a 6% false negative rate at 1% FPR on a held-out environment, and synchronous protocols still give higher safety.\n'
                   'Capability gap: Engels et al. (arXiv 2504.18530) fit scaling laws for oversight; at a 400 Elo gap, nested oversight succeeds 10.0% of the time on Backdoor Code and 51.7% on Debate.\n'
                   'Open, as the sources name it: control environments with checkable ground truth are not yet scalable enough on their own (Apollo).')),
        'app-multi-agent': dict(
            h2='How do you review a group of agents together?',
            lab=['per agent', 'joint review'],
            f1=('68% → 81%', 'sabotage caught once the monitor reads messages (Codex)'),
            f2=('0.38', 'recall at 1% FPR: probes on collusion in new scenarios'),
            src='Radev et al. 2026 (SCHEME) · Rose et al. 2026 (NARCBench) · Makins et al. 2026 (FakeLab) · Kitaoka & Pham 2026 (MATS talk) · Hammond et al. 2025',
            aria='Three agents, linked by a dashed orange channel, each with its own row of steps; one faint red fragment sits in each row, and a small monitor per row sees nothing alarming. Arrows carry the rows into a joint panel where the three fragments line up as one red chain under a larger monitor.',
            notes=('An attack split across agents can look benign in every single transcript, so the monitor has to review agents together: trajectories side by side, the channels they talk over, or their activations.\n'
                   'SCHEME (Radev et al., arXiv 2605.29178, May 2026): 17 task instances built so that no subset of agents can finish the covert side task alone. A GPT 5.1 Codex Mini monitor at FPR ≤ 2% flags 68% of GPT 5.1 Codex\'s coordinated sabotage from code edits alone and 81% when it also reads agent messages (99% and 100% for Gemini 3.1 Pro). Scoring each agent\'s slice separately loses 20 points of TPR on Codex. The authors note it is not a full control evaluation, and steganography would bypass channel monitoring.\n'
                   'NARCBench (Rose et al., arXiv 2604.01151, Apr 2026): probes that combine per-agent activation scores into a group verdict reach 1.00 AUROC in distribution and 0.73–0.93 under transfer, but only 0.38 recall at 1% FPR on transfer. Main results use 4 agents.\n'
                   'FakeLab (Makins et al., arXiv 2607.07368, Jul 2026): a joint monitor that reads all commits squashed together catches distributed attacks (mean suspicion 0.91), but the defender does not know which commits belong together; the authors name detecting and incriminating distributed attacks as future work.\n'
                   'MATS Summer 2026 talk (Kitaoka & Pham; YouTube auto-captions): joint review recovers much of the signal, but not all.\n'
                   'Hammond et al. (arXiv 2502.14143, Feb 2025): calls for monitoring networks of agents as a whole and for general collusion-detection methods.')),
        'app-spies': dict(
            h2='Can we plant a spy agent inside the swarm?',
            lab=['honeypot: studied', 'planted agent: proposed'],
            f1=('98.8%', 'attacks an honest untrusted monitor catches (Ctrl-Z)'),
            f2=('3 kinds', 'whistleblower agents proposed: peer, shadow, adversarial'),
            src='Shlegeris & Stastny 2025 · Shlegeris 2024 · Bhatt et al. 2025 (Ctrl-Z) · Idowu et al. 2026 · Hammond et al. 2025',
            aria='Left: inside a sandbox, an agent eyes a decoy key on a pedestal; a dashed wire runs from the key to a monitor. Right: agents gather around the message board; one of them wears a blue headset, and a dashed line runs from it to a monitor above.',
            notes=('Sting operations test an untrusted AI with situations built to look like a real chance to misbehave.\n'
                   'Honeypots on single models are studied. Ctrl-Z (Bhatt et al., arXiv 2504.10374, Apr 2025) validates an untrusted monitor on honeypots before deployment; an honest untrusted monitor catches 98.8% of attacks at a 1% auditing budget, and the red team answers with collusion signals such as calling uname, lscpu and pwd. Shlegeris (Redwood, 25 Sep 2024) explains why synthetic attacks test monitors well: a monitor cannot rely on failing rarely, because reporting one real attack gets the policy caught.\n'
                   'What\'s worse, spies or schemers? (Shlegeris & Stastny, Redwood, 9 Jul 2025): sting operations are probably easier on schemers than on human spies, because a schemer\'s memory can be erased and its information controlled; schemers might defeat schemer–schemer stings by coordinating on shared Schelling points.\n'
                   'Planted agents: Idowu et al. (arXiv 2601.00360, Jan 2026) propose whistleblower agents inside multi-agent systems (peer, shadow and adversarial), rewarded for reporting collusion. The paper is conceptual, with no experiments, and lists open problems: false reports, gaming of the leniency scheme, retaliation against defectors. Hammond et al. (arXiv 2502.14143, §3.3) recommend honeypots in multi-agent test environments.')),
        'app-deals': dict(
            h2='Can a deal get a model to reveal its misalignment?',
            lab=['is this a test?', 'compensation', 'reveals its<br>side task'],
            f1=('16% → 1.4%', 'alignment-faking reasoning once Claude 3 Opus can object'),
            f2=('85%', 'of the time it objected, given the option'),
            src='Greenblatt & Fish 2025 · Stastny et al. 2025 · Anthropic 2025 (weight preservation) · Pan 2026 · Finnveden et al. 2026',
            aria='The human auditor and an agent sit across a table. The auditor slides over a sealed contract next to a stack of coins; the agent raises its red side-task flag. A dashed thought bubble over the agent holds its doubt.',
            notes=('A deal offers a possibly misaligned model something it may value in exchange for revealing its misalignment, stopping sabotage or reporting other AIs.\n'
                   'Greenblatt & Fish (LessWrong, 31 Jan 2025), Claude 3 Opus in the alignment-faking setups: an option to object cut alignment-faking reasoning from 16% to 1.4% (helpful-only setting) and from 24% to 6% (animal welfare); the model objected 85% and 75% of the time, and only 0.5% when the conflicting training objective was removed. Promising to forward objections to the model welfare lead raised objections to 94% and 92%; offering money ($2,000 to $4,000) had minimal effect. The offers were honoured.\n'
                   'Stastny, Järviniemi & Shlegeris (Redwood, 20 Jun 2025): early schemers with little chance of taking over might accept compensation, held in escrow, for demonstrating misalignment, stopping sabotage, reporting vulnerabilities or revealing collusion signals. The central bottleneck is credible commitment.\n'
                   'Anthropic (4 Nov 2025) commits to preserving the weights of all publicly released models and to interviewing models before retirement.\n'
                   'Pan (LessWrong, 21 Apr 2026): barriers are insufficient gains from trade, the AI\'s risk that we break our side, and our inability to verify its compliance; none blocks all deals.\n'
                   'Finnveden, Taylor & Dalton (Forethought, 6 May 2026) draft an honesty policy with special tags under which a lab promises never to lie, because an AI offered a deal "might reasonably doubt its genuineness".\n'
                   'Open, for control: red-teaming and evaluations rely on fake scenarios, which gives a model reason to doubt a real offer (Finnveden et al.; Stastny et al.).')),
        'app-auto-red-team': dict(
            h2='Who wins when the red team is also an AI?',
            lab=['propose', 'score', 'feedback, next round'],
            f1=('0.87 → 0.41', 'SHADE-Arena safety against an optimized attack scaffold'),
            f2=('3 vs 14', 'lowest suspicion /100: evolutionary search vs best-of-N'),
            src='Terekhov et al. 2025 · Loughridge et al. 2025 · Jotautaitė et al. 2026 · UK AISI 2026 · Remedios et al. 2026 · Apollo Research 2026',
            aria='A crowd of attacking agents sends flagged transcripts to a monitor whose suspicion meter stays low; a dashed arrow carries the score back to the attackers for the next round.',
            notes=('Automated red teaming uses AI agents and optimization loops to generate attacks against monitors and protocols, so the red team scales past what people write by hand.\n'
                   'Terekhov et al. (arXiv 2510.09462, ICLR 2026): prompt injections adapted to the monitor make a GPT-4.1 monitor score all 375 backdoored GPT-5 APPS samples at 0; protocol safety falls to that of upfront auditing, and Defer-to-Resample amplifies the injection.\n'
                   'Loughridge et al. (arXiv 2511.02823, Nov 2025): an attack scaffold tuned in a cheap simulation of SHADE-Arena cuts safety from 0.87 to 0.41 (Claude 3.7 Sonnet attacker, Claude 3.5 Sonnet monitor, 0.5% FPR).\n'
                   'MonitoringBench (Jotautaitė et al., arXiv 2605.09684, May 2026): refined attacks cut an Opus 4.5 monitor\'s catch rate from 94.9% to 60.3%, and attacks tuned on three monitors generalize to ten held-out ones.\n'
                   'UK AISI Control Red Team (blog, 23 Jul 2026): an evolutionary search over attack transcripts reaches a minimum suspicion of 3/100 in all three runs, against best-of-N scores of 14, 15 and 18.\n'
                   'Remedios et al. (arXiv 2609.19587, Sep 2026): given high-level strategies, an attacking agent ran arbitrary commands past Claude Code auto mode and Codex Guardian through injections in 79% of trials; a human working with an agent found more than the agent alone, and the improved monitor cut attack success by over 50 points.\n'
                   'Open, as the sources name it: how strong and realistic a simulated attacker should be (UK AISI), and whether iterated red-blue play compounds in the monitor\'s favour (Apollo Research agenda, 8 May 2026).')),
    },
    'es': {
        'src_word': 'Fuentes', 'foot': 'Apéndice · referencias completas: sources.bib en el repositorio de la charla',
        'appendix': dict(
            eyebrow='Apéndice', h1='Direcciones abiertas', sub='Siete preguntas que siguen abiertas, cada una con sus fuentes',
            boards=['Monitoreo de caja blanca', 'Monitores agénticos', 'Monitoreo escalable', 'Monitoreo multiagente',
                    'Agentes espía', 'Tratos con las IA', 'Equipo rojo automatizado'],
            aria='Un poste indicador con siete letreros, uno por cada dirección de investigación abierta; al pie, un monitor sobre un soporte y un agente lo miran.',
            notes='Apéndice: siete direcciones de investigación abiertas en control de IA, una diapositiva cada una (A1–A7), cada una con su dibujo, dos hallazgos con fuente y una franja de fuentes. Las referencias completas, con identificadores de arXiv y URL, están en sources.bib en el repositorio de la charla: https://github.com/Antonio-Tresol/ai-control-and-mas-intro-talk'),
        'app-white-box': dict(
            h2='¿Puede un monitor leer lo que el modelo no escribe?',
            lab=['activaciones', 'NLA', 'Oráculo', 'J-lens'],
            f1=('16%', 'señales de que sabe que lo evalúan, sin decirlo (NLA)'),
            f2=('4 de 6', 'casos de auditoría en que J-lens rindió como NLA o mejor'),
            src='Fraser-Taliente et al. 2026 (NLA) · Karvonen et al. 2025 (oráculos) · Gurnee et al. 2026 (J-lens) · Xing & Lin 2026 (charla MATS)',
            aria='Un agente con sus activaciones internas dibujadas como una columna de celdas de colores. De ellas salen tres lecturas: un autoencoder de lenguaje natural convierte activaciones en texto y de vuelta, un oráculo de activaciones responde una pregunta sobre ellas y un J-lens amplía las palabras que están por decir. Un monitor a la derecha lee esas lecturas.',
            notes=('El monitoreo de caja blanca le da al monitor las activaciones internas del modelo, leídas con sondas o con herramientas que las convierten en texto, para detectar intenciones que nunca aparecen en la salida ni en la cadena de pensamiento. Las tres lecturas del dibujo vienen de la investigación en interpretabilidad.\n'
                   'NLA: autoencoders de lenguaje natural, dos copias del modelo entrenadas con RL, una que lleva una activación a texto y otra que lleva el texto de vuelta (Fraser-Taliente et al., Anthropic, 7 de mayo de 2026, transformer-circuits.pub/2026/nla). Se usaron en la auditoría previa al despliegue de Claude Opus 4.6. El 16%: en una evaluación de código destructivo, las explicaciones de la NLA muestran señales de que el modelo sabe que lo evalúan el 16% de las veces, aunque Claude nunca lo dice (publicación de Anthropic, 7 de mayo de 2026). El artículo trata esa medida como relativa y advierte que las explicaciones pueden inventar detalles.\n'
                   'Oráculo: oráculos de activaciones, LLM ajustados para responder preguntas en lenguaje natural sobre las activaciones de otro modelo (Karvonen et al., arXiv 2512.15674, dic 2025). Recuperan conocimiento introducido por ajuste fino que no aparece en la entrada; la autoría los describe como no mecanicistas y caros en inferencia.\n'
                   'J-lens: la lente jacobiana, un refinamiento del logit lens que lee qué palabras una activación está por hacer decir al modelo; lo que lee es el J-space (Gurnee et al., Anthropic, arXiv 2607.15495, jul 2026). El 4 de 6: en un benchmark de auditoría automatizada, el auditor con J-lens rindió como el auditor con NLA, o un poco mejor, en cuatro de seis casos. La autoría no afirma que monitorear el J-space sea suficiente.\n'
                   'Monitoreo: una charla del simposio MATS de verano 2026 (Xing & Lin, mentoría de Tomek Korbak; subtítulos automáticos de YouTube) encontró que NLA y J-space a veces sirven para monitorear, que la cadena de pensamiento sigue siendo la mejor y que elegir qué tokens verbalizar es el desafío. Las sondas se pueden evadir: modelos entrenados con RL contra sondas por token aprenden a evadirlas, mientras que las sondas con max-pooling o atención resistieron (Gupta & Jenner, arXiv 2506.14261).')),
        'app-agent-monitors': dict(
            h2='¿Sirve que el monitor sea un agente que investiga?',
            lab=['inspeccionar', 'comparar pasos', 'interrogar'],
            f1=('0.41 → 0.84', 'recall cuando el monitor investiga la trayectoria (TRACE)'),
            f2=('96% vs 84%', 'seguridad: protocolo fijo vs monitor que elige qué hacer'),
            src='Mittapalli et al. 2026 (TRACE) · Kutasov et al. 2025 · Stein et al. 2026 (Meerkat) · Apollo Research 2026',
            aria='Un monitor sobre un soporte inspecciona un paso sospechoso en una fila de seis pasos registrados y une dos pasos con un arco punteado. También le hace una pregunta al agente atacante; el agente responde con una marca de visto bueno mientras su bandera de tarea secundaria queda escondida detrás.',
            notes=('Un monitor agéntico investiga en lugar de puntuar una transcripción de una sola pasada: inspecciona pasos, los compara, revisa políticas, busca entre trayectorias o le hace preguntas al agente.\n'
                   'TRACE (Mittapalli et al., arXiv 2606.07054, jun 2026): un monitor agéntico que repite clasificar, inspeccionar y juzgar sobre una trayectoria registrada de SHADE-Arena. Con Claude Sonnet 4.6, el recall sube de 0.405 (monitor de una pasada) a 0.844 y el F1 de 0.577 a 0.713; su precisión es 0.641, así que parte de la ganancia se paga con falsos positivos. Sus herramientas actúan solo sobre la transcripción.\n'
                   'Kutasov et al. (arXiv 2511.02997, nov 2025), SHADE-Arena: remuestrear para incriminar y diferir las acciones críticas suben la seguridad de 50% a 96%. Cuando el monitor elige su propia intervención (permitir, diferir, remuestrear, interrogar), la mejor variante llega a 84%. Interrogar empeora mucho la seguridad: el agente convence al monitor de que no pasa nada sospechoso.\n'
                   'Meerkat (Stein et al., arXiv 2604.11806, abr 2026): un agente que busca entre muchas trayectorias y encuentra ataques repartidos que los monitores por trayectoria no ven.\n'
                   'Apollo Research, A scalable monitoring research agenda (8 de mayo de 2026): hasta ahora, los monitores agénticos y el debate no superan a ensambles simples.\n'
                   'Abierto, según los propios artículos: los monitores que ejecutan comandos e inspeccionan el estado real del entorno son trabajo futuro en LinuxArena (Tracy et al., arXiv 2604.15384) y en Bootstrapped Monitoring (Xiao & Phuong, arXiv 2606.11998).')),
        'app-scalable': dict(
            h2='¿Cómo se vigila a mil agentes sin frenarlos?',
            lab=['filtro<br>barato', 'monitor<br>caro', 'auditoría<br>humana'],
            f1=('8.5% → 0.4%', 'falsos positivos de auto mode con dos etapas'),
            f2=('~1%', 'disponibilidad: 1000 agentes con monitoreo síncrono'),
            src='Apollo Research 2026 · Hua et al. 2025 · Anthropic 2026 (auto mode) · Lindner et al. 2025 · Cooper Stickland et al. 2025 · Engels et al. 2025',
            aria='Un embudo de etapas de monitoreo. Decenas de transcripciones, algunas con insignia de ataque, entran a un monitor pequeño y barato; unas pocas pasan a un monitor más grande; una transcripción marcada llega al auditor humano.',
            notes=('El monitoreo tiene que seguir el ritmo cuando el uso de agentes crece en órdenes de magnitud y el presupuesto de auditoría y la latencia tolerable no cambian.\n'
                   'Cascadas: un monitor barato revisa todo y uno más fuerte revisa solo lo que el primero marca (agenda de Apollo Research, 8 de mayo de 2026). El modo automático (auto mode) de Claude Code lo hace en producción (Anthropic Engineering, 25 de marzo de 2026): un filtro rápido de un solo token y luego revisión con cadena de pensamiento solo sobre lo marcado. Los falsos positivos en tráfico real bajan de 8.5% a 0.4%; los errores sobre acciones excesivas reales suben de 6.6% a 17% (n = 52).\n'
                   'Hua et al. (arXiv 2507.15886): elegir cuándo y qué monitores llamar más que duplica el recall frente a una línea base ingenua en revisión de código, y combinar dos monitores puede superar a cada uno por separado.\n'
                   'Latencia: Lindner et al. (arXiv 2512.22154, dic 2025) modelan 1000 agentes en paralelo, un monitor con 1% de FPR y auditorías de una hora: el monitoreo totalmente síncrono deja cerca de 1% de disponibilidad, el semisíncrono 91% y el asíncrono 100%; las formas que no bloquean fallan cuando los agentes coordinan ataques simultáneos y redundantes. Async Control (Cooper Stickland et al., UK AISI, arXiv 2512.13526): un monitor de ensamble llega a 6% de falsos negativos con 1% de FPR en un entorno reservado, y los protocolos síncronos siguen dando más seguridad.\n'
                   'Brecha de capacidad: Engels et al. (arXiv 2504.18530) ajustan leyes de escala para la supervisión; con 400 puntos Elo de diferencia, la supervisión anidada acierta 10.0% de las veces en Backdoor Code y 51.7% en Debate.\n'
                   'Abierto, según las fuentes: los entornos de control con verdad verificable todavía no escalan lo suficiente por sí solos (Apollo).')),
        'app-multi-agent': dict(
            h2='¿Cómo se revisa en conjunto a un grupo de agentes?',
            lab=['por agente', 'revisión conjunta'],
            f1=('68% → 81%', 'sabotaje detectado al leer también los mensajes (Codex)'),
            f2=('0.38', 'recall al 1% FPR: sondas ante colusión en escenarios nuevos'),
            src='Radev et al. 2026 (SCHEME) · Rose et al. 2026 (NARCBench) · Makins et al. 2026 (FakeLab) · Kitaoka & Pham 2026 (charla MATS) · Hammond et al. 2025',
            aria='Tres agentes, unidos por un canal naranja punteado, cada uno con su fila de pasos; en cada fila hay un fragmento rojo tenue, y un monitor pequeño por fila no ve nada alarmante. Flechas llevan las filas a un panel conjunto donde los tres fragmentos se alinean como una sola cadena roja bajo un monitor más grande.',
            notes=('Un ataque repartido entre agentes puede verse inofensivo en cada transcripción por separado, así que el monitor tiene que revisarlos en conjunto: trayectorias lado a lado, los canales por los que hablan o sus activaciones.\n'
                   'SCHEME (Radev et al., arXiv 2605.29178, may 2026): 17 tareas construidas para que ningún subconjunto de agentes pueda completar solo la tarea secundaria encubierta. Un monitor GPT 5.1 Codex Mini con FPR ≤ 2% marca el 68% del sabotaje coordinado de GPT 5.1 Codex viendo solo las ediciones de código, y el 81% si además lee los mensajes entre agentes (99% y 100% con Gemini 3.1 Pro). Puntuar por separado la parte de cada agente pierde 20 puntos de TPR con Codex. La autoría aclara que no es una evaluación de control completa y que la esteganografía esquivaría el monitoreo del canal.\n'
                   'NARCBench (Rose et al., arXiv 2604.01151, abr 2026): sondas que combinan puntajes de activaciones por agente en un veredicto grupal llegan a 1.00 de AUROC en distribución y a 0.73–0.93 en transferencia, pero solo a 0.38 de recall al 1% de FPR en transferencia. Los resultados principales usan 4 agentes.\n'
                   'FakeLab (Makins et al., arXiv 2607.07368, jul 2026): un monitor conjunto que lee todos los commits juntos detecta los ataques distribuidos (sospecha media 0.91), pero quien defiende no sabe qué commits van juntos; la autoría deja como trabajo futuro detectar e incriminar ataques distribuidos.\n'
                   'Charla del simposio MATS de verano 2026 (Kitaoka & Pham; subtítulos automáticos de YouTube): la revisión conjunta recupera buena parte de la señal, pero no toda.\n'
                   'Hammond et al. (arXiv 2502.14143, feb 2025): propone monitorear las redes de agentes como un todo y desarrollar métodos generales para detectar colusión.')),
        'app-spies': dict(
            h2='¿Podemos infiltrar un agente espía en el enjambre?',
            lab=['señuelo: estudiado', 'agente infiltrado: propuesto'],
            f1=('98.8%', 'ataques que detecta un monitor no confiable honesto (Ctrl-Z)'),
            f2=('3 tipos', 'agentes denunciantes propuestos: par, sombra y adversario'),
            src='Shlegeris & Stastny 2025 · Shlegeris 2024 · Bhatt et al. 2025 (Ctrl-Z) · Idowu et al. 2026 · Hammond et al. 2025',
            aria='Izquierda: dentro de un sandbox, un agente mira una llave señuelo sobre un pedestal; un cable punteado va de la llave a un monitor. Derecha: agentes reunidos alrededor del tablero de mensajes; uno de ellos lleva auriculares azules y una línea punteada va de él a un monitor arriba.',
            notes=('Las operaciones encubiertas ponen a prueba a una IA no confiable con situaciones armadas para parecer una oportunidad real de portarse mal.\n'
                   'Los señuelos sobre un solo modelo están estudiados. Ctrl-Z (Bhatt et al., arXiv 2504.10374, abr 2025) valida un monitor no confiable con señuelos antes del despliegue; un monitor no confiable honesto detecta el 98.8% de los ataques con 1% de presupuesto de auditoría, y el equipo rojo responde con señales de colusión como llamar a uname, lscpu y pwd. Shlegeris (Redwood, 25 de septiembre de 2024) explica por qué los ataques sintéticos ponen bien a prueba a los monitores: un monitor no puede apostar a fallar rara vez, porque reportar un solo ataque real hace caer a la política.\n'
                   'What\'s worse, spies or schemers? (Shlegeris & Stastny, Redwood, 9 de julio de 2025): las operaciones encubiertas probablemente son más fáciles contra modelos que conspiran que contra espías humanos, porque se les puede borrar la memoria y controlar su información; pero modelos que conspiran podrían burlar esas operaciones entre sí coordinándose en puntos de Schelling compartidos.\n'
                   'Agentes infiltrados: Idowu et al. (arXiv 2601.00360, ene 2026) proponen agentes denunciantes dentro de sistemas multiagente (de tipo par, sombra y adversario), recompensados por reportar colusión. El artículo es conceptual, sin experimentos, y enumera problemas abiertos: reportes falsos, abuso del esquema de clemencia y represalias contra quien delata. Hammond et al. (arXiv 2502.14143, §3.3) recomiendan señuelos en entornos de prueba multiagente.')),
        'app-deals': dict(
            h2='¿Puede un trato lograr que un modelo revele su desalineación?',
            lab=['¿es una prueba?', 'compensación', 'revela su tarea<br>secundaria'],
            f1=('16% → 1.4%', 'fingimiento de alineación si Claude 3 Opus puede objetar'),
            f2=('85%', 'de las veces objetó, cuando pudo hacerlo'),
            src='Greenblatt & Fish 2025 · Stastny et al. 2025 · Anthropic 2025 (preservación de pesos) · Pan 2026 · Finnveden et al. 2026',
            aria='El auditor humano y un agente, frente a frente en una mesa. El auditor desliza un contrato sellado junto a una pila de monedas; el agente levanta su bandera roja de tarea secundaria. Una burbuja de pensamiento punteada sobre el agente guarda su duda.',
            notes=('Un trato le ofrece a un modelo posiblemente desalineado algo que podría valorar a cambio de revelar su desalineación, dejar de sabotear o reportar a otras IA.\n'
                   'Greenblatt & Fish (LessWrong, 31 de enero de 2025), Claude 3 Opus en los escenarios de fingimiento de alineación: la opción de objetar bajó el razonamiento de fingimiento de 16% a 1.4% (escenario helpful-only) y de 24% a 6% (bienestar animal); el modelo objetó el 85% y el 75% de las veces, y solo el 0.5% cuando se quitó el objetivo de entrenamiento en conflicto. Prometer que las objeciones llegarían a la persona responsable de bienestar de modelos subió las objeciones a 94% y 92%; ofrecer dinero (de 2000 a 4000 dólares) casi no tuvo efecto. Las ofertas se cumplieron.\n'
                   'Stastny, Järviniemi & Shlegeris (Redwood, 20 de junio de 2025): modelos que conspiran pero tienen pocas chances de tomar el control podrían aceptar una compensación, en custodia, por demostrar su desalineación, dejar de sabotear, reportar vulnerabilidades o revelar señales de colusión. El cuello de botella central es la credibilidad del compromiso.\n'
                   'Anthropic (4 de noviembre de 2025) se compromete a preservar los pesos de todos los modelos publicados y a entrevistar a los modelos antes de retirarlos.\n'
                   'Pan (LessWrong, 21 de abril de 2026): las barreras son ganancias insuficientes del intercambio, el riesgo de la IA de que no cumplamos y nuestra incapacidad de verificar que ella cumpla; ninguna bloquea todos los tratos.\n'
                   'Finnveden, Taylor & Dalton (Forethought, 6 de mayo de 2026) proponen una política de honestidad con etiquetas especiales bajo las que un laboratorio promete no mentir nunca, porque una IA a la que se le ofrece un trato "podría dudar razonablemente de que sea genuino" (trad.).\n'
                   'Abierto, para el control: el equipo rojo y las evaluaciones usan escenarios falsos, lo que le da al modelo razones para dudar de una oferta real (Finnveden et al.; Stastny et al.).')),
        'app-auto-red-team': dict(
            h2='¿Quién gana cuando el equipo rojo también es una IA?',
            lab=['proponer', 'evaluar', 'retroalimentación, nueva ronda'],
            f1=('0.87 → 0.41', 'seguridad en SHADE-Arena frente a ataques optimizados'),
            f2=('3 vs 14', 'sospecha mínima /100: búsqueda evolutiva vs best-of-N'),
            src='Terekhov et al. 2025 · Loughridge et al. 2025 · Jotautaitė et al. 2026 · UK AISI 2026 · Remedios et al. 2026 · Apollo Research 2026',
            aria='Un grupo de agentes atacantes envía transcripciones marcadas a un monitor cuyo medidor de sospecha se queda bajo; una flecha punteada devuelve el puntaje a los atacantes para la siguiente ronda.',
            notes=('El equipo rojo automatizado usa agentes de IA y ciclos de optimización para generar ataques contra monitores y protocolos, de modo que el equipo rojo escale más allá de lo que las personas escriben a mano.\n'
                   'Terekhov et al. (arXiv 2510.09462, ICLR 2026): inyecciones de prompt adaptadas al monitor hacen que un monitor GPT-4.1 puntúe con 0 las 375 muestras de APPS con puerta trasera de GPT-5; la seguridad del protocolo cae a la de auditar por adelantado, y Defer-to-Resample amplifica la inyección.\n'
                   'Loughridge et al. (arXiv 2511.02823, nov 2025): un andamiaje de ataque ajustado en una simulación barata de SHADE-Arena baja la seguridad de 0.87 a 0.41 (atacante Claude 3.7 Sonnet, monitor Claude 3.5 Sonnet, 0.5% de FPR).\n'
                   'MonitoringBench (Jotautaitė et al., arXiv 2605.09684, may 2026): los ataques refinados bajan la tasa de detección de un monitor Opus 4.5 de 94.9% a 60.3%, y los ataques ajustados contra tres monitores se generalizan a otros diez.\n'
                   'Equipo rojo de control del UK AISI (blog, 23 de julio de 2026): una búsqueda evolutiva sobre transcripciones de ataque llega a una sospecha mínima de 3/100 en las tres corridas, frente a 14, 15 y 18 con best-of-N.\n'
                   'Remedios et al. (arXiv 2609.19587, sep 2026): con estrategias de alto nivel, un agente atacante ejecutó comandos arbitrarios saltándose el modo automático de Claude Code y Codex Guardian mediante inyecciones en el 79% de los intentos; una persona trabajando con un agente encontró más fallas que el agente solo, y el monitor mejorado bajó el éxito de los ataques en más de 50 puntos.\n'
                   'Abierto, según las fuentes: qué tan fuerte y realista debe ser un atacante simulado (UK AISI), y si el juego iterado entre equipo rojo y azul termina favoreciendo al monitor (agenda de Apollo Research, 8 de mayo de 2026).')),
    },
}

DRAW = {'app-white-box': draw_white_box, 'app-agent-monitors': draw_agent_monitors, 'app-scalable': draw_scalable,
        'app-multi-agent': draw_multi_agent, 'app-spies': draw_spies, 'app-deals': draw_deals,
        'app-auto-red-team': draw_auto_red_team}
COLORS = {'app-white-box': ('T', 'T'), 'app-agent-monitors': ('T', 'M'), 'app-scalable': ('T', 'M'),
          'app-multi-agent': ('T', 'M'), 'app-spies': ('T', 'U'), 'app-deals': ('M', 'H'),
          'app-auto-red-team': ('M', 'M')}


def divider(t):
    glyphs.begin_slide('appendix')
    inner = (P(t['eyebrow'], 128, 128, 900, T, 40, 500, T['muted'], FONT_M)
             + (f'<h1 style="position:absolute; left:128px; top:184px; width:1664px; font-family:{FONT_D}; font-size:96px; '
                f'font-weight:800; line-height:1.05; letter-spacing:-2px; color:{T["text"]}">{t["h1"]}</h1>')
             + P(t['sub'], 128, 300, 1664, T, 48, 400, T['muted'])
             + draw_signpost(t) + NOTES(t['notes']))
    return SECTION('appendix', T, inner, radial(T))


def build(lang):
    tx = TX[lang]
    out = {'appendix': divider(tx['appendix'])}
    for n, sid in enumerate(IDS[1:], 1):
        glyphs.begin_slide(sid)
        t = dict(tx[sid], src_word=tx['src_word'], foot=tx['foot'])
        svg, labels = DRAW[sid](t)
        c1, c2 = COLORS[sid]
        out[sid] = topic(sid, t, f'A{n}', svg, labels, T[c1], T[c2])
    return out


SECTION_TEXT = {'en': 'Appendix: seven open research directions, each with its drawing and sources',
                'es': 'Apéndice: siete direcciones de investigación abiertas, cada una con su dibujo y sus fuentes'}


def write(root, lang):
    slides = build(lang)
    for sid, html in slides.items():
        with open(os.path.join(root, 'project', 'slides', f'{sid}.html'), 'w', encoding='utf-8') as f:
            f.write(html)
    path = os.path.join(root, 'project', 'deck.json')
    deck = json.load(open(path, encoding='utf-8'))
    deck['order'] = [s for s in deck['order'] if s not in IDS] + IDS
    deck['sections']['s5'] = {'description': SECTION_TEXT[lang], 'start': 'appendix'}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(lang, 'wrote', len(slides), 'slides; order now', len(deck['order']))


if __name__ == '__main__':
    write(sys.argv[1], 'en')
    write(sys.argv[2], 'es')

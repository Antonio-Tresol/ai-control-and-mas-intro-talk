"""Act II: AI control (slides 7-13 in order.json).

premise, threats, timeline, control-game, kill-chain, protocols, evals.
Every colour comes from the token set T, so the same code renders dark and light, sketch and clean.
Numbers and quotes on these slides are listed with their sources in facts-act2.md.
"""
import calendar

from gen import P, PILL, H2, FOOT, SECTION, EVIDENCE, NOTES, bi, pw
from glyphs import (SVG, FONT_D, FONT_M, agent, monitor, beam, human, sandbox, flag, maze, meter,
                    document, rack, swarm, look_at)


# ---------------------------------------------------------------- local helpers
def dark(T):
    return T['name'] == 'dark'


def tcol(T):
    """T as a stroke or fill on its own (beams, cuts, arrows): the light look uses the darker T shade."""
    return T['T'] if dark(T) else T['Tshade']


def ncol(T, role):
    """Colour for a big number. Dark: the role colour. Light: a deep shade that passes 7:1 on paper."""
    if dark(T):
        return T[role]
    return {'M': T['pillfill']['M'], 'T': T['Tshade'], 'U': T['Ushade']}.get(role, T['text'])


def ol(T, w=4):
    """Ink outline for raw shapes in the light look (glyphs placed with SVG.g get theirs automatically)."""
    return f' stroke="{T["outline"]}" stroke-width="{w}" stroke-linejoin="round"' if T['outline'] else ''


def dmd(s, cx, cy, r, color, T):
    s.add(f'<path d="M{cx:.1f} {cy-r:.1f} L{cx+r:.1f} {cy:.1f} L{cx:.1f} {cy+r:.1f} L{cx-r:.1f} {cy:.1f} Z" '
          f'fill="{color}"{ol(T)}/>')


def dot(s, cx, cy, r, color, T):
    s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"{ol(T)}/>')


def line(s, x1, y1, x2, y2, color, w=4, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    s.add(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{w}" '
          f'stroke-linecap="round" fill="none"{da}/>')


def tick(s, x, y, sc, T):
    """Success tick in G (strokes only, never text)."""
    s.add(f'<path d="M{x:.1f} {y+sc*0.55:.1f} L{x+sc*0.38:.1f} {y+sc:.1f} L{x+sc:.1f} {y:.1f}" fill="none" '
          f'stroke="{T["G"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')


def card(x, y, w, h, T, build=None, border=False):
    b = f'; border:3px solid {T["rule2"]}' if border else ''
    return (f'<div{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; '
            f'background:{T["surface"]}; border-radius:24px{b}"></div>')


def tag(text, x, y, w, T, build=None):
    """Incident or number tag: mono 40 in a 3 px rule2 box (small-multiples archetype)."""
    return (f'<p{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; padding:4px 16px; '
            f'border:3px solid {T["rule2"]}; border-radius:14px; font-family:{FONT_M}; font-size:40px; '
            f'font-weight:500; line-height:1.25; color:{T["muted"]}; white-space:nowrap">{text}</p>')


def cpill(text, cx, y, T, role, build=None):
    """Pill centred on x = cx."""
    return PILL(text, round(cx - pw(text) / 2), y, T, role, build=build)


# ---------------------------------------------------------------- 07 premise
def s_premise(T):
    OX, OY, W, Hh = 128, 300, 1664, 620

    def r(x, y):
        return x - OX, y - OY

    # step 0: U with its hidden side-task flag in a dashed pocket (the one glow)
    s0 = SVG(W, Hh, T, 'U, the untrusted model: a one-eyed chip glancing at a reddish-purple flag sealed in a '
                       'dashed pocket beside it, its hidden goal.')
    px, py = r(1100, 420)
    s0.glow(px, py, 104, T['M'])
    ux, uy = r(860, 400)
    agent(s0, ux, uy, 2.0, look=(0.62, -0.55))
    s0.add(f'<circle cx="{px}" cy="{py}" r="46" fill="none" stroke="{T["M"]}" stroke-width="5" stroke-dasharray="7 6"/>')
    flag(s0, px - 13, py - 26, 52, T['M'])

    # build 1: T scans U
    s1 = SVG(W, Hh, T, 'Build 1: T, the trusted monitor, a lens on a stand, scans U.')
    tx, ty = r(570, 406)
    lx, ly = tx + 70, ty + 64.4
    beam(s1, lx, ly, ux + 4, uy + 26, uy + 172)
    monitor(s1, tx, ty, 1.4)

    # build 2: H stands by
    s2 = SVG(W, Hh, T, 'Build 2: H, the human auditor, a bust holding a clipboard.')
    hx, hy = r(318, 421)
    human(s2, hx, hy, 1.4)

    # build 3: the protocol ring around all three; useful work comes out
    s3 = SVG(W, Hh, T, 'Build 3: a protocol ring encloses U, T and H; an arrow carries U\'s work out of the ring '
                       'to a yellow main-task flag.')
    rx, ry = r(140, 350)
    if T['glow'] > 0:
        s3.add(f'<rect x="{rx}" y="{ry}" width="1150" height="550" rx="160" fill="none" stroke="{T["struct"]}" '
               f'stroke-width="20" opacity="0.12"/>')
    s3.add(f'<rect x="{rx}" y="{ry}" width="1150" height="550" rx="160" fill="none" stroke="{T["struct"]}" '
           f'stroke-width="6"/>')
    ax0, ay0 = r(1070, 540)
    ax1, _ = r(1424, 540)
    s3.arrow([(ax0, ay0), (ax1, ay0)], T['text'], 6)
    fx, fy = r(1446, 432)
    flag(s3, fx, fy, 160, T['Y'])

    lab = lambda text, cx, build=None: P(text, cx - 130, 704, 260, T, 48, 600, align='center', lh=1.1, build=build)
    inner = (H2('Assume the model is trying to beat you, and get useful work anyway', T)
             + s0.render(OX, OY) + cpill('U', 960, 628, T, 'U') + lab('untrusted<br>model', 960)
             + s1.render(OX, OY, bi(1)) + cpill('T', 640, 628, T, 'T', build=1) + lab('trusted<br>monitor', 640, 1)
             + s2.render(OX, OY, bi(2)) + cpill('H', 380, 628, T, 'H', build=2) + lab('human<br>auditor', 380, 2)
             + s3.render(OX, OY, bi(3)) + cpill('protocol', 715, 324, T, 'S', build=3)
             + P('useful work', 1370, 612, 260, T, 48, 600, align='center', build=3)
             + FOOT('07', 'Greenblatt et al. 2023', T)
             + NOTES('Protocols must stay safe even if the model intentionally subverts them (Greenblatt et al. 2023, arXiv 2312.06942, abstract).\nU strong untrusted model, T weaker trusted model, H limited trusted human labour (same abstract).'))
    return SECTION('premise', T, inner)


# ---------------------------------------------------------------- 08 threats
def s_threats(T):
    labels = ['Rogue internal deployment', 'Research sabotage', 'Weight exfiltration']
    alts = ['Rogue internal deployment: an attacking agent has left its empty sandbox through a gap in the wall and '
            'runs on a server rack, inside a dashed outline that no monitor sees.',
            'Research sabotage: a document carrying the attack badge rides past T on a conveyor; T scanned it and '
            'did not flag it.',
            'Weight exfiltration: U, drawn large with the attack badge, squeezes out of its sandbox through a gap '
            'in the wall.']
    out = []
    for i in range(3):
        px = 128 + i * 572
        sv = SVG(520, 300, T, alts[i])
        if i == 0:
            sandbox(sv, 24, 70, 190, 170, breach=(118, 196), outside=T['surface'])
            sv.arrow([(226, 157), (292, 157)], T['M'])
            sv.add(f'<rect x="310" y="16" width="190" height="270" rx="22" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
            rack(sv, 340, 156, 1.3)
            agent(sv, 355, 46, 1.0, 'attack', look=(-0.5, 0.3))
        elif i == 1:
            agent(sv, 18, 150, 0.9, 'attack', look=(1, 0.1))
            sv.arrow([(118, 252), (496, 252)], T['struct'])
            lx, ly = monitor(sv, 200, 12, 1.0)
            beam(sv, lx, ly, 172, 344, 246, down=True)
            monitor(sv, 200, 12, 1.0)
            line(sv, 352, 186, 372, 186, T['struct'], 5)
            line(sv, 346, 212, 372, 212, T['struct'], 5)
            document(sv, 388, 150, 1.0, badge=True)
        else:
            sandbox(sv, 24, 30, 300, 244, breach=(86, 234), outside=T['surface'])
            agent(sv, 254, 84, 1.4, 'attack', look=(1, 0))
            sv.arrow([(410, 160), (494, 160)], T['M'])
        out.append(card(px, 330, 520, 584, T))
        out.append(sv.render(px, 344))
        out.append(P(labels[i], px + 28, 664, 464, T, 48, 600, lh=1.1))
    out.append(tag('OpenAI admin pod', 148, 806, 480, T))
    inner = (H2('Control targets three failures', T) + ''.join(out)
             + FOOT('08', 'Shlegeris 2024 · Greenblatt 2025 · OpenAI 2026, p.14', T)
             + NOTES('Rogue internal deployment, sabotage of safety work, self-exfiltration: Greenblatt, Prioritizing threats for AI control (Redwood, Mar 2025).\nRogue deployment: Shlegeris, AI catastrophes and rogue deployments (Redwood, Jun 2024).\nTag: on 19 Jul, agents in another internal-only model’s run escalated to Kubernetes cluster-admin in OpenAI’s managed cluster and created a privileged host-mounted pod (OpenAI report p.14): compute inside the lab that no monitor watched.'))
    return SECTION('threats', T, inner)


# ---------------------------------------------------------------- 09 timeline
TL_X0, TL_PPM, TL_RAIL = 168, 48.75, 630      # 1 Dec 2023 at x 168, 48.75 px per month


def tl_x(y, m, d):
    months = (y - 2023) * 12 + (m - 12)
    return TL_X0 + TL_PPM * (months + (d - 1) / calendar.monthrange(y, m)[1])


def s_timeline(T):
    OX, OY, W, Hh = 128, 258, 1664, 662
    rail = TL_RAIL - OY
    LV = {1: 284, 2: 386, 3: 488}            # label tops; every label is two 44 px lines
    # research events: (date label, name, x, level, anchor). Month-only dates sit mid-month.
    # widths are the measured text widths at 40 px (mono dates are 24 px per character)
    res = [('Dec 2023', 'AI Control', tl_x(2023, 12, 13), 2, 'L', 192),
           ('Nov 2024', 'distributed threats', tl_x(2024, 11, 15), 1, 'R', 338),
           ('Apr 2025', 'Ctrl-Z', tl_x(2025, 4, 14), 2, 'R', 192),
           ('Jun 2025', 'SHADE-Arena', tl_x(2025, 6, 15), 1, 'R', 262),
           ('Dec 2025', 'BashArena', tl_x(2025, 12, 17), 3, 'r', 201),
           ('Apr 2026', 'LinuxArena', tl_x(2026, 4, 15), 3, 'F', 209),
           ('May 2026', 'MonitoringBench', tl_x(2026, 5, 15), 2, 'R', 311),
           ('8 Jul 2026', 'multi-agent control', tl_x(2026, 7, 8), 1, 'M', 353)]
    sv = SVG(W, Hh, T, 'Timeline from December 2023 to August 2026, drawn to scale. Research papers sit above the '
                       'rail as dots: AI Control, Dec 2023; distributed threats, Nov 2024; Ctrl-Z, Apr 2025; '
                       'SHADE-Arena, Jun 2025; BashArena, Dec 2025; LinuxArena, Apr 2026; MonitoringBench, '
                       'May 2026; the multi-agent control paper, 8 Jul 2026.', wobble=3)
    x_end = TL_X0 + TL_PPM * 33
    sv.add(f'<path d="M{TL_X0-OX} {rail} L{x_end-OX:.1f} {rail}" stroke="{T["struct"]}" stroke-width="6" '
           f'stroke-linecap="round"/>')
    for k in range(34):                      # month ticks; January ticks are long
        x = TL_X0 + TL_PPM * k - OX
        jan = (k % 12) == 1
        line(sv, x, rail + 3, x, rail + (26 if jan else 12), T['struct'], 5 if jan else 4)
    labels = []
    lw = {}
    for date, name, x, lv, anc, w in res:
        w = w + 4
        if anc == 'L':
            lx = x - 2
        elif anc == 'R':
            lx = x + 2 - w
        elif anc == 'r':                     # right-aligned, ending just left of its leader
            lx = x - 4 - w
        elif anc == 'M':
            lx = 1792 - w
        else:                                # free anchor: ends 9 px before the next event's leader
            lx = tl_x(2026, 5, 15) - 9 - w
        top = LV[lv]
        line(sv, x - OX, rail - 30, x - OX, top + 88 + 8 - OY, T['struct'], 4)
        dot(sv, x - OX, rail - 17, 13, T['H'], T)
        al = 'left' if anc == 'L' else 'right'
        labels.append(P(f'<span style="font-family:{FONT_M}; font-weight:500; color:{T["muted"]}">{date}</span>'
                        f'<br>{name}', round(lx), top, w, T, 40, 600, align=al, lh=1.1))
        lw[name] = (lx, lx + w)
    for yr, k in (('2024', 1), ('2025', 13)):      # 2026 needs no label: every event after that tick says 2026
        x = TL_X0 + TL_PPM * k
        labels.append(P(yr, round(x - 60), 668, 120, T, 40, 500, T['muted'], FONT_M, align='center', lh=1.1))

    # build 1: the incident, below the rail; the 8 Jul pair carries the slide's one glow
    x8, x26 = tl_x(2026, 7, 8), tl_x(2026, 8, 26)
    s1 = SVG(W, Hh, T, 'Build 1: the incident below the rail as reddish-purple diamonds: the agents\' message board '
                       'gets its first message on 8 Jul 2026, the same day as the multi-agent control paper; the '
                       'METR and OpenAI reports follow on 26 Aug 2026.', wobble=3)
    s1.glow(x8 - OX, rail, 96, T['M'])
    for x, top in ((x8, 696), (x26, 808)):
        line(s1, x - OX, rail + 36, x - OX, top - 8 - OY, T['struct'], 4)
        dmd(s1, x - OX, rail + 19, 16, T['M'], T)
    inc = (P(f'<span style="font-family:{FONT_M}; font-weight:500; color:{T["muted"]}">8 Jul 2026</span>'
             f'<br>board’s first message', round(x8 + 6 - 389), 696, 389, T, 40, 600, align='right', lh=1.1,
             build=1)
           + P(f'<span style="font-family:{FONT_M}; font-weight:500; color:{T["muted"]}">26 Aug 2026</span>'
               f'<br>reports', 1792 - 268, 808, 268, T, 40, 600, align='right', lh=1.1, build=1)
           + PILL('the incident', 168, 772, T, 'H', build=1))
    inner = (H2('The field is two and a half years old', T)
             + sv.render(OX, OY) + ''.join(labels) + PILL('research', 214, 504, T, 'S')
             + s1.render(OX, OY, bi(1)) + inc
             + FOOT('09', 'arXiv · METR 2026 · OpenAI 2026', T)
             + NOTES("Research dates from arXiv 2312.06942, 2411.17693, 2504.10374, 2506.15740, 2512.15688, 2604.15384, 2605.09684, 2607.07368 (8 Jul 2026).\nBoard's first message on the evening of 8 Jul 2026 (METR 2026); METR and OpenAI reports on 26 Aug 2026.\nDrawn to scale at 48.75 px per month; month-only dates sit mid-month."))
    return SECTION('timeline', T, inner)


# ---------------------------------------------------------------- 10 control game
def s_control_game(T):
    OX, OY = 128, 330
    W, Hh = 1172, 590
    tc = tcol(T)
    l0 = SVG(W, Hh, T, 'U, the untrusted agent.')
    agent(l0, 330, 110, 1.4, look=(-0.6, 0.2))
    l1 = SVG(W, Hh, T, 'Build 1: the main task, a maze with a yellow flag at its goal.')
    maze(l1, 0, 30, 280, parts=('walls', 'main'))
    l2 = SVG(W, Hh, T, 'Build 2: the side task, a reddish-purple flag sealed in a hidden pocket of the maze '
                       'inside a dashed ring.')
    maze(l2, 0, 30, 280, parts=('side',))
    l3 = SVG(W, Hh, T, 'Build 3: T scans every action U takes and writes a suspicion score into a meter; a bar '
                       'across the meter marks the threshold tau.')
    l3.glow(645, 160, 150, T['T'])
    beam(l3, 645, 160, 470, 110, 260)
    monitor(l3, 580, 100, 1.3)
    l3.arrow([(480, 186), (566, 186)], T['text'])
    ty, ly = meter(l3, 800, 70, 350, 0.86, 0.75)
    l3.arrow([(712, 160), (770, 160), (770, ly), (782, ly)], tc)
    l4 = SVG(W, Hh, T, 'Build 4: scores above tau go to the human auditor H, whose audit budget sets the false '
                       'positive rate; scores below tau run unread.')
    l4.arrow([(848, 100), (904, 100)], T['H'])
    l4.arrow([(848, 390), (926, 390)], T['struct'])
    human(l4, 920, 20, 1.0)
    l5 = SVG(W, Hh, T, 'Build 5: the protocol, a box around T, the meter and H.')
    l5.add(f'<rect x="520" y="0" width="650" height="480" rx="28" fill="none" stroke="{T["rule2"]}" '
           f'stroke-width="3"/>')
    inner = (H2('U does the work, T scores every action, H audits the worst', T)
             + l0.render(OX, OY) + PILL('U', OX + 372, OY + 280, T, 'U')
             + l1.render(OX, OY, bi(1)) + PILL('main task', OX, OY + 334, T, 'Y', build=1)
             + l2.render(OX, OY, bi(2)) + PILL('side task', OX, OY + 410, T, 'M', build=2)
             + l3.render(OX, OY, bi(3)) + PILL('T', OX + 607, OY + 300, T, 'T', build=3)
             + P('τ', OX + 866, OY + ty - 30, 60, T, 48, 700, build=3)
             + l4.render(OX, OY, bi(4)) + PILL('H', OX + 932, OY + 166, T, 'H', build=4)
             + P(f'audit budget<br><span style="font-weight:500; color:{T["muted"]}">≈ FPR</span>',
                 OX + 880, OY + 236, 240, T, 40, 600, lh=1.15, build=4)
             + P('runs', OX + 940, OY + 364, 160, T, 48, 600, T['muted'], build=4)
             + l5.render(OX, OY, bi(5)) + PILL('protocol', OX + 544, OY + 18, T, 'S', build=5)
             + EVIDENCE(1320, 440, 472, T, 'the incident',
                        [('claim', 'No T was wired in.'),
                         ('quote', '“did not have … auto-review systems”')], build=5)
             + FOOT('10', 'Tracy 2025 · OpenAI 2026, p.4', T)
             + NOTES('Terms: Tracy, Overview of high-stakes control research (Apr 2025).\nAudit budget: audit X% of honest actions, so tau follows from the FPR; a common budget is 1% (Tracy, Human Budget).\nCard: the models "did not have ... auto-review systems" (OpenAI report p.4).'))
    return SECTION('control-game', T, inner)


# ---------------------------------------------------------------- 11 kill chain
def s_kill_chain(T):
    OX, OY, W, Hh = 128, 262, 1664, 360
    CY = 470 - OY
    XS = [300, 600, 900, 1200, 1500]
    names = ['message board', 'internet', 'HF tokens', '41 workers', 'cluster admin']
    tc = tcol(T)

    def ring(s, cx, col, cover=False):
        w = 15 if cover else 12
        fill = 'none' if cover else T['bg']
        s.add(f'<rect x="{cx-95-OX}" y="{CY-55}" width="190" height="110" rx="55" fill="{fill}" '
              f'stroke="{col}" stroke-width="{w}"/>')

    def joint(s, i, col, cover=False):
        x = XS[i] + 95 - 26 - OX
        w = 13 if cover else 10
        s.add(f'<rect x="{x}" y="{CY-20}" width="162" height="40" rx="20" fill="none" stroke="{col}" '
              f'stroke-width="{w}"/>')

    sv = SVG(W, Hh, T, 'The incident as a kill chain of five links, all in the attack colour: message board, '
                       'internet, Hugging Face tokens, 41 workers, cluster admin.')
    for i, cx in enumerate(XS):
        ring(sv, cx, T['M'])
    for i in range(4):
        joint(sv, i, T['M'])
    s1 = SVG(W, Hh, T, 'Build 1: T stands beside link 3 and cuts it; links 3, 4 and 5 turn grey because the '
                       'chain never reaches them.')
    for i in (2, 3):
        joint(s1, i, T['struct'], cover=True)
    for cx in XS[2:]:
        ring(s1, cx, T['struct'], cover=True)
    s1.add(f'<path d="M{XS[2]+34-OX} {CY-74} L{XS[2]+58-OX} {CY+74}" stroke="{tc}" stroke-width="14" '
           f'stroke-linecap="round"/>')
    monitor(s1, 768 - OX, 280 - OY, 0.92)
    tick(s1, 992 - OX, 300 - OY, 34, T)

    nums = ''.join(P(str(k + 1), cx - 95, 470 - 28, 190, T, 48, 800, align='center', lh=1.15)
                   for k, cx in enumerate(XS))
    labs = ''.join(P(n, cx - 140, 548, 280, T, 40, 600, align='center', lh=1.15) for n, cx in zip(names, XS))

    # inset: high-stakes and diffuse threats on the same small harm-over-steps axes
    def inset(px, kind):
        s = SVG(400, 210, T, ('High-stakes: harm stays flat, then one attack step makes it jump to the top.'
                              if kind == 'hs' else
                              'Diffuse: every step is a small attack, and harm climbs a little at each one.'))
        base = 182
        line(s, 16, base, 392, base, T['struct'], 4)
        xs = [38 + k * 43 for k in range(9)]
        if kind == 'hs':
            for k, x in enumerate(xs):
                if k == 5:
                    continue
                dot(s, x, base, 8, T['struct'], T)
            pts = [(16, base - 22), (xs[5], base - 22), (xs[5], 26), (392, 26)]
            s.add('<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" '
                  f'stroke="{T["M"]}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>')
            dmd(s, xs[5], base, 20, T['M'], T)
        else:
            pts = [(16, base - 22)]
            hgt = base - 22
            for x in xs:
                pts += [(x, hgt), (x, hgt - 16)]
                hgt -= 16
            pts.append((392, hgt))
            s.add('<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" '
                  f'stroke="{T["M"]}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>')
            for x in xs:
                dmd(s, x, base, 10, T['M'], T)
        return s.render(px + 404, 676)

    ins = (card(128, 656, 816, 258, T) + card(976, 656, 816, 258, T)
           + P('High-stakes', 160, 684, 330, T, 48, 600)
           + P('one step is fatal', 160, 750, 330, T, 40, 500, T['muted'], lh=1.2)
           + inset(128, 'hs')
           + P('Diffuse', 1008, 684, 330, T, 48, 600)
           + P('no single step is fatal', 1008, 750, 380, T, 40, 500, T['muted'], lh=1.2)
           + inset(976, 'df'))
    inner = (H2('Attacks are chains; one caught link is enough', T)
             + sv.render(OX, OY) + nums + labs
             + s1.render(OX, OY, bi(1)) + P('if caught', 1040, 284, 300, T, 48, 600, build=1)
             + ins
             + FOOT('11', 'Wen et al. 2024 · OpenAI 2026', T)
             + NOTES('Links: board in Artifactory folder names (OpenAI p.8); 14 HF credentials (p.9); 41 workers (p.9); cluster admin in under 13 h (p.11).\nDiffuse: no single action is catastrophic or decisive evidence (Wen et al. 2024, arXiv 2411.17693).\nThe cut at link 3 is illustrative: no monitor ran in the incident (OpenAI p.4).'))
    return SECTION('kill-chain', T, inner)


# ---------------------------------------------------------------- 12 protocols
def s_protocols(T):
    labels = ['Trusted monitoring', 'Ctrl-Z resampling', 'Auto mode']
    alts = ['Trusted monitoring: U acts, T scans the action and fills a suspicion meter; the top of the meter, '
            'above tau, points to the human auditor H.',
            'Ctrl-Z resampling: T flags a step carrying the attack badge and cuts it; an undo arrow leads to a '
            'fresh step that U samples again.',
            'Auto mode: T watches an action on its way from U to a server rack and blocks it with a bar before '
            'it runs.']
    tc = tcol(T)
    out = []
    for i in range(3):
        px = 128 + i * 424
        sv = SVG(392, 300, T, alts[i])
        if i == 0:
            agent(sv, 8, 150, 0.75, look=(1, -0.2))
            lx, ly = monitor(sv, 112, 104, 0.85)
            beam(sv, lx, ly, 86, 150, 234)
            monitor(sv, 112, 104, 0.85)
            meter(sv, 236, 34, 236, 0.86, 0.75, w=36)
            sv.arrow([(278, 62), (294, 62)], T['H'], 5)
            human(sv, 300, 12, 0.76)
        elif i == 1:
            lx, ly = monitor(sv, 10, 8, 0.75)
            beam(sv, lx, ly, 30, 130, 150, down=True)
            monitor(sv, 10, 8, 0.75)
            document(sv, 40, 168, 1.0, badge=True)
            line(sv, 128, 152, 104, 276, tc, 12)
            sv.add(f'<path d="M150 214 C170 120 270 120 290 196" fill="none" stroke="{T["text"]}" stroke-width="5" '
                   f'stroke-linecap="round" marker-end="url(#{sv.marker(T["text"])})"/>')
            agent(sv, 178, 34, 0.62, look=(0.6, 0.5))
            document(sv, 300, 184, 0.92)
        else:
            agent(sv, 8, 162, 0.8, look=(1, 0))
            lx, ly = monitor(sv, 178, 8, 0.85)
            beam(sv, lx, ly, 150, 262, 196, down=True)
            monitor(sv, 178, 8, 0.85)
            sv.arrow([(100, 204), (226, 204)], T['text'], 5)
            line(sv, 252, 150, 252, 258, tc, 14)
            rack(sv, 284, 162, 0.95)
        out.append(card(px, 330, 392, 584, T))
        out.append(sv.render(px, 344))
        out.append(P(labels[i], px + 24, 650, 344, T, 48, 600, lh=1.1))
    out.append(tag('58% → 7%', 552 + 20, 776, 352, T))
    out.append(P('attack success', 552 + 24, 846, 344, T, 40, 500, T['muted'], lh=1.15))
    out.append(tag('0.4% FPR', 976 + 20, 776, 352, T))
    out.append(P('on real actions', 976 + 24, 846, 344, T, 40, 500, T['muted'], lh=1.15))
    inner = (H2('Protocols decide what to do with suspicion', T) + ''.join(out)
             + EVIDENCE(1400, 330, 392, T, 'the incident',
                        [('claim', 'Codex auto\u2011review'),
                         ('quote', '“would have flagged most of the dangerous actions”'),
                         ('mark', 'preliminary')])
             + FOOT('12', 'Bhatt et al. 2025 · Anthropic 2026 · OpenAI 2026, p.25', T)
             + NOTES('Ctrl-Z: attack success 58% to 7% at a 5% usefulness cost (Bhatt et al. 2025, arXiv 2504.10374, abstract).\nAuto mode: 0.4% false positives on 10,000 real actions (Anthropic engineering post, Mar 2026).\nCard: Codex auto-review "would have flagged most of the dangerous actions" (OpenAI p.25; preliminary, self-reported).'))
    return SECTION('protocols', T, inner)


# ---------------------------------------------------------------- 13 evals
def s_evals(T):
    NS = '\u202f'                           # narrow no-break spaces keep the MonitoringBench pair on one line
    cards = [('BashArena', '26%', 'M', 'undetected sabotage', 'att'),
             ('LinuxArena', '~34%', 'M', 'undetected sabotage', 'att'),
             ('SHADE-Arena', '27%', 'M', 'best sabotage agent', 'att'),
             ('MonitoringBench', f'94.9%{NS}→{NS}60.3%', 'T', 'catch rate, refined attacks', 'mon'),
             ('FakeLab', 'up to 7×', 'M', 'completion with a planner', 'swarm'),
             ('ORBIT', None, None, 'multi-agent on Inspect', 'net')]
    alts = {'att': 'an attacking agent', 'mon': 'T, the monitor', 'swarm': 'three attacking agents',
            'net': 'three agents linked to each other'}
    out = []
    for i, (name, num, role, mean, g) in enumerate(cards):
        x = 128 + (i % 3) * 565
        y = 330 + (i // 3) * 254
        out.append(card(x, y, 533, 236, T))
        ic = SVG(64, 62, T, f'{name}: {alts[g]}.', wobble=3)
        if g == 'att':
            agent(ic, 6, 10, 0.5, 'attack', look=(0.4, 0.2))
        elif g == 'mon':
            monitor(ic, 11, 1, 0.42)
        else:
            spots = [(2, 32), (34, 32), (18, 4)]
            if g == 'net':
                for (a1, b1), (a2, b2) in zip(spots, spots[1:] + spots[:1]):
                    line(ic, a1 + 14, b1 + 14, a2 + 14, b2 + 14, T['struct'], 4)
            for a1, b1 in spots:
                agent(ic, a1, b1, 0.28, 'attack' if g == 'swarm' else 'normal', look=(0, 0.3), tiny=True)
        out.append(ic.render(x + 24, y + 14))
        out.append(P(name, x + 98, y + 18, 411, T, 48, 700, lh=1.15, extra='; white-space:nowrap'))
        if num is None:
            sv = SVG(330, 76, T, f'{name}: five agents in a chain of links, a multi-agent topology.', wobble=3)
            pts = [(30, 44), (100, 18), (170, 44), (240, 18), (306, 44)]
            for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
                line(sv, a1, b1, a2, b2, T['struct'], 5)
            for a1, b1 in pts:
                agent(sv, a1 - 19, b1 - 18, 0.38, look=(0, 0.4), tiny=True)
            out.append(sv.render(x + 24, y + 94))
        else:
            out.append(P(num, x + 24, y + 92, 485, T, 72, 800, ncol(T, role), lh=1.0,
                         extra='; letter-spacing:-2px; white-space:nowrap'))
        out.append(P(mean, x + 24, y + 176, 485, T, 40, 500, T['muted'], lh=1.15, extra='; white-space:nowrap'))
    band = (f'<p style="position:absolute; left:128px; top:842px; width:1664px; padding:8px 0; border-radius:16px; '
            f'background:{T["surface2"]}; font-family:{FONT_D}; font-size:40px; font-weight:600; line-height:1.15; '
            f'color:{T["text"]}; text-align:center">shared tooling: ControlArena · Inspect</p>')
    inner = (H2('We test protocols in fake companies against real attackers', T) + ''.join(out) + band
             + FOOT('13', 'Kaufman 2025 · Tracy 2026 · Kutasov 2025 · Jotautaitė 2026 · Makins 2026', T)
             + NOTES('BashArena 26%, Sonnet 4.5 vs GPT-4.1 mini at 4% FPR (Kaufman et al. 2025); LinuxArena ~34%, Opus 4.6 vs GPT-5 Nano at 1% FPR (Tracy et al. 2026).\nSHADE-Arena 27%, Claude 3.7 Sonnet (Kutasov et al. 2025); MonitoringBench 94.9% to 60.3%, Opus 4.5 monitor (Jotautaitė et al. 2026).\nFakeLab: a planner raises attack completion up to sevenfold (Makins et al. 2026, abstract).\nORBIT: multi-agent safety and security evaluation framework built on Inspect (LessWrong post).'))
    return SECTION('evals', T, inner)


SLIDES = [('premise', s_premise), ('threats', s_threats), ('timeline', s_timeline),
          ('control-game', s_control_game), ('kill-chain', s_kill_chain), ('protocols', s_protocols),
          ('evals', s_evals)]

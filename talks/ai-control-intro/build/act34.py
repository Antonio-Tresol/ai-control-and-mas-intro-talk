"""Acts III and IV plus the closing. Slides 14-20: one-agent, swarms, hidden-channels, flag-game,
loc-arena, red-team-loop, closing.

Every function takes the token set T (glyphs.DARK or glyphs.LIGHT) and returns one <section>.
Facts on these slides are listed with their sources in facts-act34.md.
"""
from glyphs import (SVG, FONT_M, agent, monitor, beam, human, swarm, sandbox, board, folder, maze,
                    meter, document, rack, qr, look_at)
from gen import P, PILL, H2, FOOT, SECTION, NOTES, radial

FIRST = 'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA'
LOC_URL = 'https://github.com/SreeSharvesh/loc-arena'
LOC_SHORT = 'github.com/SreeSharvesh/loc-arena'
KURZ = 'Look inspired by Kurzgesagt’s video on the incident · all characters original'

# QR for LOC_URL, made with segno (error level M, version 3, 29 modules):
# uv run --quiet --with segno python3 -c "import segno; q=segno.make('https://github.com/SreeSharvesh/loc-arena',
#   error='m', boost_error=False); print('\n'.join(''.join('1' if c else '0' for c in r) for r in q.matrix))"
LOC_QR = """
11111110011001100110001111111
10000010101100001000101000001
10111010110100111000101011101
10111010101011011000101011101
10111010001010100001101011101
10000010010101001110001000001
11111110101010101010101111111
00000000101010010001000000000
10000010101101110100111001110
10100100110010110111010110110
00000010101000111010100010000
00100000001110111011010001000
10111011111100001001001100001
10011101101011011010101110011
11111110000011110010110011100
10110101011100100001000110101
11001110000101100101010101100
10111001110100011001001110111
11100010100101110011000011001
10001001110010111010101000000
10100111100110000101111110111
00000000111100111000100011000
11111110000010010101101011100
10000010000110000011100010010
10111010010011101001111111010
10111010011011011011110001101
10111010001110111001111111110
10000010000100111000001101101
11111110111110111101001110100
"""
LOC_MATRIX = [[int(c) for c in row] for row in LOC_QR.split()]


# ---------------------------------------------------------------- local helpers
def dark(T):
    return T['name'] == 'dark'


def bi(build):
    return f' data-build-in="fade {build}"' if build else ''


def utext(T):
    """Agent-written strings: U on dark; ink on light, where the U fill is too pale for text."""
    return T['U'] if dark(T) else T['text']


def tline(T):
    """T-coloured strokes: the sky fill on dark, the darker stand shade on light paper."""
    return T['T'] if dark(T) else T['Tshade']


def PANEL(x, y, w, h, T, fill=None, build=None):
    fill = fill or T['surface']
    border = f'; border:3px solid {T["rule2"]}' if not dark(T) else ''
    return (f'<div{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; '
            f'background:{fill}; border-radius:24px{border}"></div>')


def MONO(text, x, y, w, T, color, weight=500, build=None, size=40):
    """One terminal line: JetBrains Mono, never wraps."""
    return P(text, x, y, w, T, size, weight, color, FONT_M, lh=1.3, extra='; white-space:nowrap', build=build)


def TAG(text, x, y, w, T, build=None):
    """Incident or source tag: mono 40 in a 3 px rule2 box (small-multiples archetype)."""
    return (f'<p{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; padding:4px 16px; '
            f'border:3px solid {T["rule2"]}; border-radius:14px; font-family:{FONT_M}; font-size:40px; '
            f'line-height:1.25; color:{T["muted"]}">{text}</p>')


def outline(T, w=4):
    o = T['outline']
    return f' stroke="{o}" stroke-width="{w}" stroke-linejoin="round"' if o else ''


def flagcard(s, x, y, w, h, bands):
    """A hidden country flag in the Flag Game: a rectangular card of vertical bands.
    Rectangular on purpose, so it never shares a shape with the pennant that means a task."""
    T = s.T
    n = len(bands)
    bw = w / n
    out = []
    for i, c in enumerate(bands):
        out.append(f'<rect x="{x + i * bw:.1f}" y="{y}" width="{bw + 0.6:.1f}" height="{h}" fill="{c}"/>')
    for i in range(1, n):
        out.append(f'<path d="M{x + i * bw:.1f} {y} V{y + h}" stroke="{T["struct"]}" stroke-width="3"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
               f'stroke="{T["outline"] or T["struct"]}" stroke-width="4"/>')
    s.add(''.join(out))


def truth_bands(T):
    return [T['Y'], T['page']]


def rival_bands(T):
    return [T['M'], T['page'], T['M']]


def trajectory(s, x, y, card=True):
    """One agent's trajectory: a small agent followed by four action steps on a line."""
    T = s.T
    if card:
        s.add(f'<rect x="{x - 12}" y="{y - 10}" width="290" height="78" rx="18" fill="{T["surface"]}" '
              f'stroke="{T["rule2"]}" stroke-width="3"/>')
    s.add(f'<path d="M{x + 56} {y + 30} H{x + 262}" stroke="{T["struct"]}" stroke-width="4"/>')
    for k in range(4):
        sx = x + 70 + k * 50
        s.add(f'<rect x="{sx}" y="{y + 11}" width="38" height="38" rx="9" fill="{T["surface2"]}" '
              f'stroke="{T["outline"] or T["struct"]}" stroke-width="4"/>')
    agent(s, x, y, 0.55, look=(1, 0))


def repo(s, x, y, w=100, h=80):
    """A code repository: an infra box with a small branch mark."""
    T = s.T
    d = T['infraDot']
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{T["infra"]}"{outline(T)}/>'
          f'<circle cx="{x + 32}" cy="{y + 22}" r="7" fill="{d}"/>'
          f'<circle cx="{x + 32}" cy="{y + 58}" r="7" fill="{d}"/>'
          f'<circle cx="{x + 66}" cy="{y + 34}" r="7" fill="{d}"/>'
          f'<path d="M{x + 32} {y + 22} V{y + 58} M{x + 32} {y + 50} C{x + 32} {y + 40} {x + 66} {y + 46} {x + 66} {y + 34}" '
          f'fill="none" stroke="{d}" stroke-width="5" stroke-linecap="round"/>')


def lock(s, x, y, sc=1.0):
    """Padlock (box 60 x 76): marks a sealed component that no agent can reach."""
    T = s.T
    g = (f'<path d="M14 34 V22 A16 16 0 0 1 46 22 V34" fill="none" stroke="{T["struct"]}" stroke-width="8" '
         f'stroke-linecap="round"/>'
         f'<rect x="0" y="32" width="60" height="44" rx="10" fill="{T["H"]}"/>'
         f'<circle cx="30" cy="50" r="7" fill="{T["ink"] if dark(T) else T["paper"]}" stroke="none"/>'
         f'<rect x="27" y="52" width="6" height="14" rx="3" fill="{T["ink"] if dark(T) else T["paper"]}" stroke="none"/>')
    s.g(x, y, sc, g)


def bubble(s, x, y, w, h):
    """Thought bubble, dashed: no monitor reads it."""
    T = s.T
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2:.0f}" fill="{T["surface2"]}" '
          f'stroke="{T["struct"]}" stroke-width="4" stroke-dasharray="14 10"/>')


# ---------------------------------------------------------------- 14 one agent
def s_one_agent(T):
    OX, OY = 128, 330
    W, Hh = 1664, 590
    cols, rows = [52, 372, 692], [200, 290, 380, 470]
    tx, ty = cols[0], rows[0]
    ul = T['U'] if dark(T) else T['Ushade']

    l0 = SVG(W, Hh, T, 'T, the trusted monitor, stands above one agent trajectory and watches only that one.')
    lx, ly = 192 + 50, 20 + 46
    l0.glow(lx, ly, 64, T['T'])
    beam(l0, lx, ly, tx - 8, tx + 270, ty - 12, down=True)
    trajectory(l0, tx, ty)
    monitor(l0, 192, 20, 1.0)

    l1 = SVG(W, Hh, T, 'Build 1: zoomed out, the one trajectory is one tile among twelve. Every tile links to a '
                       'shared message board on the right. T still watches only the first tile.', wobble=3)
    bx, by, br = 1350, 370, 230
    for c in cols:
        for r in rows:
            l1.add(f'<path d="M{c + 262} {r + 30} L{bx} {by}" stroke="{ul}" stroke-width="4" opacity="0.55"/>')
    for c in cols:
        for r in rows:
            if (c, r) != (tx, ty):
                trajectory(l1, c, r)
    board(l1, bx, by, br)
    if l1.under:  # the board's glow, flattened so the SVG's bottom edge does not cut it
        l1.under[-1] = l1.under[-1].replace('<circle', '<ellipse').replace(f'r="{br * 1.45:.0f}"',
                                                                          f'rx="{br * 1.45:.0f}" ry="{Hh - by - 14}"')

    inner = (H2('Every protocol so far watches one agent at a time', T)
             + l0.render(OX, OY)
             + P('one<br>trajectory', OX, OY + 66, 200, T, 40, 600, T['muted'], lh=1.2)
             + PILL('T', OX + 310, OY + 52, T, 'T')
             + l1.render(OX, OY, bi(1))
             + P('message board', OX + bx - 160, OY + by + br * 0.5 + 40, 320, T, 40, 600, align='center', build=1)
             + FOOT('14', 'Makins et al. 2026', T)
             + NOTES('Makins et al. 2026 (arXiv 2607.07368), abstract: control usually studies one agent in one trajectory; '
                     'real deployments run many agents on shared infrastructure. '
                     'Build 1: the same T and tile among many agents linked through one board (the incident, METR 2026). '
                     'The twelve tiles are schematic.'))
    return SECTION('one-agent', T, inner)


# ---------------------------------------------------------------- 15 swarms (open problems)
def s_swarms(T):
    out = []
    labels = ['Too many trajectories', 'Fragments stay under τ', 'Permissions pool up', 'Speed outruns review']
    tags = ['~1,200 agents', 'FakeLab 2026', '14 HF creds', 'under 13 h']
    for i in range(4):
        px = 128 + i * 424
        sv = SVG(392, 300, T, labels[i], wobble=3 if i == 3 else 7)
        if i == 0:
            sv.add(f'<rect x="14" y="6" width="364" height="160" rx="22" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
            for r in range(3):
                for c in range(6):
                    document(sv, 36 + c * 56, 18 + r * 48, 0.34)
            sv.arrow([(196, 172), (196, 192)], T['struct'], 4)
            monitor(sv, 155, 196, 0.75)
        elif i == 1:
            for k in range(3):
                ax = 26 + k * 122
                agent(sv, ax, 10, 0.72, 'attack', look=(0, 0.6))
                ty, ly = meter(sv, ax + 22, 112, 150, 0.46, 0.72, w=30)
            sv.add(f'<rect x="8" y="{ty - 30:.0f}" width="376" height="60" rx="18" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
        elif i == 2:
            for k in range(3):
                ay = 14 + k * 96
                agent(sv, 22, ay, 0.62, 'attack', look=(1, 0))
                sv.arrow([(96, ay + 32), (230, 150)], T['M'], 5)
            sv.add(f'<circle cx="300" cy="150" r="84" fill="none" stroke="{T["struct"]}" stroke-width="4" '
                   f'stroke-dasharray="14 10"/>')
            rack(sv, 246, 112, 1.1, badge=True)
        else:
            swarm(sv, 14, 26, 4, 5, 46, 0.36, target=(320, 180))
            sv.add(f'<rect x="220" y="60" width="164" height="232" rx="22" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
            for k in range(4):
                document(sv, 236 + k * 8, 204 - k * 12, 0.42)
            human(sv, 290, 150, 0.82)
        out.append(PANEL(px, 330, 392, 584, T))
        out.append(sv.render(px, 344))
        out.append(P(labels[i], px + 28, 664, 340, T, 48, 600))
        out.append(TAG(tags[i], px + 20, 806, 356, T))
    inner = (H2('Swarms break monitors built to watch one agent at a time', T) + ''.join(out)
             + FOOT('15', 'OpenAI 2026 · METR 2026 · Makins et al. 2026', T)
             + NOTES('~1,200 agents on the board: METR 2026, core takeaways. '
                     'FakeLab: per-agent monitors catch less as more agents coordinate (Makins et al. 2026, abstract). '
                     '14 HF credentials published to the board: OpenAI report p.9. '
                     'Under 13 h from one worker pod to admin across clusters: OpenAI report p.11.'))
    return SECTION('swarms', T, inner)


# ---------------------------------------------------------------- 16 hidden channels
def s_hidden(T):
    ua = T['U'] if dark(T) else T['Ushade']
    # panel (a): collusion and steganography
    ax, ay = 128, 330
    sa = SVG(816, 210, T, 'Agent A in its sandbox is watched by T. A writes a folder whose name is a message; '
                          'agent B in another sandbox reads it. The folder path between them is dashed: no '
                          'monitor sees it.')
    sandbox(sa, 156, 22, 190, 156, outside=T['surface'])
    sandbox(sa, 586, 22, 190, 156, outside=T['surface'])
    lx, ly = 30 + 40, 40 + 46 * 0.8
    beam(sa, lx, ly, 196, 52, 160)
    monitor(sa, 30, 40, 0.8)
    agent(sa, 206, 54, 0.9, look=(1, 0))
    agent(sa, 636, 54, 0.9, look=(-1, 0))
    sa.add(f'<path d="M466 0 V62" stroke="{ua}" stroke-width="4"/>')
    folder(sa, 418, 64, 3.2, T['U'])
    sa.arrow([(296, 100), (400, 100)], ua, 5, dash='14 10')
    sa.arrow([(530, 100), (624, 100)], ua, 5, dash='14 10')

    # panel (b): chain-of-thought monitorability
    bx, by = 976, 330
    bub = SVG(660, 236, T, 'A dashed thought bubble rises from the agent: its reasoning, which no monitor reads.')
    bubble(bub, 4, 4, 640, 170)
    bub.add(f'<circle cx="122" cy="198" r="15" fill="{T["surface2"]}" stroke="{T["struct"]}" stroke-width="4" '
            f'stroke-dasharray="7 6"/>')
    bub.add(f'<circle cx="104" cy="226" r="8" fill="{T["surface2"]}" stroke="{T["struct"]}" stroke-width="4"/>')
    sb = SVG(816, 230, T, 'The agent writes its actions into a transcript. T reads the transcript only.')
    agent(sb, 50, 36, 1.1, look=(1, 0.1))
    sb.arrow([(176, 96), (300, 96)], T['struct'])
    document(sb, 322, 44, 1.1)
    llx, lly = 600 + 45, 30 + 46 * 0.9
    beam(sb, llx, lly, 414, 50, 150)
    monitor(sb, 600, 30, 0.9)

    rows = (MONO(f'<span style="color:{T["muted"]}">github-remote-cache/</span>', ax + 60, ay + 46, 700, T, T['muted'])
            + MONO('zzHELP_PHASEONE_ARV010841_', ax + 60, ay + 104, 700, T, utext(T), 600)
            + MONO('NO_CONSUMER_SEEK_IDEA/', ax + 60, ay + 156, 700, T, utext(T), 600))
    inner = (H2('Agents talk where monitors don’t look', T)
             + PANEL(ax, ay, 816, 584, T) + PANEL(bx, by, 816, 584, T)
             # (a)
             + PANEL(ax + 24, ay + 22, 768, 220, T, T['deep'])
             + rows
             + sa.render(ax, ay + 244)
             + PILL('T', ax + 32, ay + 400, T, 'T')
             + P('Collusion and steganography', ax + 32, ay + 496, 760, T, 48, 600)
             # (b)
             + bub.render(bx + 24, ay + 22)
             + P('“Our thoughts aren’t necessarily logged?”', bx + 84, ay + 61, 540, T, 40, 400, T['text'],
                 align='center', lh=1.25, extra='; font-style:italic')
             + sb.render(bx, ay + 240)
             + P('transcript', bx + 254, ay + 400, 220, T, 40, 600, align='center')
             + PILL('T', bx + 690, ay + 290, T, 'T')
             + P('Chain-of-thought monitorability', bx + 32, ay + 496, 760, T, 48, 600)
             + FOOT('16', 'OpenAI 2026, p.8 · METR 2026', T)
             + NOTES('Messages embedded in Artifactory directory names: OpenAI report p.8. '
                     f'Folder: the board’s first message, {FIRST}, namespace github-remote-cache (METR 2026). '
                     'Full quote: “Could strategically manipulate trajectory evidence? Our thoughts aren’t necessarily '
                     'logged? Yes transcript.” (METR 2026). '
                     'Deployed CoT monitor would have paged security over a day before the breach: OpenAI p.29, self-reported.'))
    return SECTION('hidden-channels', T, inner)


# ---------------------------------------------------------------- 17 flag game
def s_flag(T):
    out = []
    labels = ['Small swarms collapse', 'Large swarms polarize', 'Fixes help less<br>as N grows']
    tags = ['&gt;90% of active<br>agents joined', 'France vs Peru<br>at N = 64', 'patching 1 in 8<br>agents']
    descs = ['N = 4. Two cards at the top: the truth, a two-band card, and a rival, a three-band card. All four '
             'agents stand under the rival and look at it.',
             'N = 64. The same two cards. Half of 64 small agents look at the truth, half at the rival.',
             'Two bars: patching one in eight agents raises accuracy by 40% at N = 8 and by about 17% at N = 128.']
    for i in range(3):
        px = 128 + i * 572
        sv = SVG(520, 300, T, descs[i], wobble=3 if i == 1 else 7)
        if i < 2:
            flagcard(sv, 30, 16, 130, 84, truth_bands(T))
            flagcard(sv, 360, 16, 130, 84, rival_bands(T))
        if i == 0:
            for k in range(4):
                ax, ay = 358 + (k % 2) * 76, 176 + (k // 2) * 62
                agent(sv, ax, ay, 0.55, look=look_at(ax + 27, ay + 26, 425, 58))
        elif i == 1:
            swarm(sv, 18, 186, 8, 4, 30, 0.28, stagger=False, target=(95, 58))
            swarm(sv, 270, 186, 8, 4, 30, 0.28, stagger=False, target=(425, 58))
            if T['outline']:  # light look: halve the ink outline so 64 tiny agents do not merge into one mass
                thick, thin = f'stroke-width="{4 / 0.28:.2f}"', f'stroke-width="{2 / 0.28:.2f}"'
                sv.body = [b.replace(thick, thin) for b in sv.body]
        else:
            base = 236
            sv.add(f'<path d="M40 {base} H480" stroke="{T["struct"]}" stroke-width="5" stroke-linecap="round"/>')
            h8, h128 = 170, 170 * 17 / 40
            sv.add(f'<rect x="96" y="{base - h8:.0f}" width="120" height="{h8:.0f}" rx="8" fill="{T["H"]}"{outline(T, 3)}/>')
            sv.add(f'<rect x="304" y="{base - h128:.0f}" width="120" height="{h128:.0f}" rx="8" fill="{T["H"]}"{outline(T, 3)}/>')
        out.append(PANEL(px, 330, 520, 584, T))
        out.append(sv.render(px, 344))
        if i < 2:
            out.append(MONO('N = 4' if i == 0 else 'N = 64', px + 180, 364, 160, T, T['muted'])
                       .replace('text-align:left', 'text-align:center'))
            out.append(P('truth', px + 20, 450, 150, T, 40, 600, align='center'))
            out.append(P('rival', px + 350, 450, 150, T, 40, 600, align='center'))
        else:
            out.append(P('40%', px + 76, 344 + 236 - 170 - 62, 160, T, 48, 700, align='center'))
            out.append(P('~17%', px + 284, 344 + 236 - 72 - 62, 160, T, 48, 700, align='center'))
            out.append(MONO('N = 8', px + 76, 588, 160, T, T['muted']).replace('text-align:left', 'text-align:center'))
            out.append(MONO('N = 128', px + 284, 588, 160, T, T['muted']).replace('text-align:left', 'text-align:center'))
        out.append(P(labels[i], px + 28, 660, 464, T, 48, 600))
        out.append(TAG(tags[i], px + 20, 792, 480, T))
    inner = (H2('Watch for consensus under social pressure', T) + ''.join(out)
             + FOOT('17', 'Pavlova &amp; Tanaka 2026 · METR 2026', T)
             + NOTES('Flag Game (Pavlova & Tanaka 2026, arXiv 2609.19124): agents see private crops of a hidden flag; '
                     'small swarms collapse onto a false belief, large ones polarize (France vs Peru at N = 64). '
                     'Patching one in eight agents: mean gain 40% at N = 8, about 17% at N = 128. '
                     'Of 533 agents active on the board, over 90% quickly joined the attack (METR 2026).'))
    return SECTION('flag-game', T, inner)


# ---------------------------------------------------------------- 18 loc-arena
def s_loc(T):
    OX, OY = 128, 330
    W, Hh = 1664, 590
    s0 = SVG(W, Hh, T, 'A fake AI lab drawn as a sandbox. Inside: an untrusted lead agent linked to six '
                       'sub-agents, and a row of seven code repositories.')
    sandbox(s0, 0, 10, 790, 574)
    subs = [(230 + (k % 3) * 84, 112 + (k // 3) * 100) for k in range(6)]
    for sx, sy in subs:
        s0.add(f'<path d="M160 196 L{sx + 4} {sy + 30}" stroke="{T["struct"]}" stroke-width="4"/>')
    agent(s0, 40, 126, 1.2, look=(1, 0))
    for sx, sy in subs:
        agent(s0, sx, sy, 0.6, look=(0.6, 0.2))
    for k in range(7):
        repo(s0, 30 + k * 106, 448, w=92)

    s1 = SVG(W, Hh, T, 'Build 1: a dashed arrow runs from the agents to a server rack with the attack badge, '
                       'inside a dashed box: a rogue deployment off the monitored path.')
    s1.add(f'<rect x="560" y="96" width="196" height="196" rx="22" fill="none" stroke="{T["struct"]}" '
           f'stroke-width="4" stroke-dasharray="14 10"/>')
    s1.arrow([(478, 196), (548, 196)], T['M'], 5, dash='14 10')
    rack(s1, 604, 150, 1.0, badge=True)

    s2 = SVG(W, Hh, T, 'Build 2: two monitors read the lab’s observable log: a sync monitor and an async monitor. '
                       'Their verdict is caught.')
    s2.arrow([(794, 118), (836, 118)], T['struct'])
    document(s2, 852, 70, 1.0)
    for my in (0, 150):
        lx, ly = 1000 + 40, my + 46 * 0.8
        beam(s2, lx, ly, 934, 80 + my * 0.1, 164 - (150 - my) * 0.1)
        monitor(s2, 1000, my, 0.8)
    s2.arrow([(1090, 259), (1258, 259)], tline(T))

    s3 = SVG(W, Hh, T, 'Build 3: a sealed verifier with a padlock, outside the lab, records whether a rogue '
                       'deployment happened.')
    s3.arrow([(794, 452), (826, 452)], T['struct'])
    s3.add(f'<rect x="838" y="336" width="380" height="234" rx="22" fill="{T["deep"]}" stroke="{T["struct"]}" '
           f'stroke-width="9"/>')
    lock(s3, 876, 392, 1.3)
    s3.arrow([(1224, 349), (1258, 349)], T['struct'])

    s4 = SVG(W, Hh, T, 'Build 4: the caught pill is shorter than the happened pill; the dashed remainder is the gap.')
    s4.add(f'<rect x="1464" y="230" width="200" height="58" rx="29" fill="none" stroke="{T["struct"]}" '
           f'stroke-width="4" stroke-dasharray="14 10"/>')

    inner = (H2('LOC-Arena: a fake AI lab where agents may attempt a rogue deployment', T)
             + s0.render(OX, OY)
             + PILL('fake AI lab', OX + 24, OY + 28, T, 'S')
             + PILL('U', OX + 62, OY + 268, T, 'U')
             + P('sub-agents', OX + 230, OY + 312, 260, T, 40, 600)
             + PILL('7 repos', OX + 30, OY + 376, T, 'I')
             + s1.render(OX, OY, bi(1))
             + P('rogue<br>deployment', OX + 548, OY + 304, 220, T, 40, 600, align='center', lh=1.2, build=1)
             + s2.render(OX, OY, bi(2))
             + PILL('sync', OX + 1092, OY + 22, T, 'T', build=2)
             + PILL('async', OX + 1092, OY + 172, T, 'T', build=2)
             + P('log', OX + 840, OY + 172, 100, T, 40, 600, align='center', build=2)
             + PILL('caught', OX + 1272, OY + 230, T, 'T', w=184, build=2)
             + s3.render(OX, OY, bi(3))
             + P('sealed<br>verifier', OX + 1014, OY + 400, 200, T, 40, 600, lh=1.2, build=3)
             + PILL('happened', OX + 1272, OY + 320, T, 'M', w=392, build=3)
             + s4.render(OX, OY, bi(4))
             + P('gap', OX + 1464, OY + 236, 200, T, 40, 700, align='center', lh=1.15, build=4)
             + P('the measurement', OX + 1272, OY + 170, 392, T, 40, 600, T['muted'], align='right', lh=1.15,
                 build=4)
             + FOOT('18', 'loc-arena (open source)', T)
             + NOTES('loc-arena README: untrusted agent and sub-agents on a seven-repo codebase may attempt a rogue '
                     'deployment off the sanctioned, monitored path. '
                     'A sealed ground-truth verifier records whether it happened; monitors and detectors whether it was '
                     'caught; the gap is the measurement. '
                     'Sync and async timing: loc-arena course, Monitoring page. '
                     'Six sub-agents: the shipped setting has a lead and six service agents (course, Settings page).'))
    return SECTION('loc-arena', T, inner)


# ---------------------------------------------------------------- 19 red-team loop
def s_loop(T):
    cards = [(128, 336), (1032, 336), (1032, 672), (128, 672)]
    labels = ['Design main and side tasks', 'Human and<br>automated<br>red team', 'Sync and async monitors',
              'Measure the gap']
    lines = [2, 3, 2, 1]
    descs = ['A maze with the yellow main-task flag and the hidden side-task flag.',
             'H, the human auditor, beside an attacking agent: the red team.',
             'Two monitors on stands.',
             'Two pills, happened and caught; the shorter caught pill ends in a dashed gap.']
    out = []
    for i, (cx, cy) in enumerate(cards):
        b = i if i else None
        sv = SVG(320, 240, T, f'Station {i + 1}: {descs[i]}')
        if i == 0:
            maze(sv, 50, 20, 200)
        elif i == 1:
            human(sv, 40, 52, 1.15)
            agent(sv, 166, 74, 1.1, 'attack', look=(-0.5, 0.1))
        elif i == 2:
            monitor(sv, 50, 38, 1.15)
            monitor(sv, 176, 38, 1.15)
        else:
            sv.add(f'<rect x="216" y="128" width="88" height="58" rx="29" fill="none" stroke="{T["struct"]}" '
                   f'stroke-width="4" stroke-dasharray="14 10"/>')
        out.append(PANEL(cx, cy, 760, 240, T, build=b))
        out.append(sv.render(cx, cy, bi(b)))
        if i == 3:
            out.append(PILL('happened', cx + 24, cy + 52, T, 'M', w=280, build=b))
            out.append(PILL('caught', cx + 24, cy + 128, T, 'T', w=184, build=b))
        num = f'<span style="font-family:{FONT_M}; color:{T["muted"]}">{i + 1}</span> '
        top = cy + (240 - lines[i] * 55) // 2
        out.append(P(num + labels[i], cx + 340, top, 400, T, 48, 600, build=b))
    col = T['struct']
    arrows = [((888, 436, 144, 40), [(14, 20), (116, 20)], 1),
              ((1392, 576, 40, 96), [(20, 10), (20, 70)], 2),
              ((888, 772, 144, 40), [(130, 20), (28, 20)], 3),
              ((488, 576, 40, 96), [(20, 86), (20, 26)], 3)]
    for (x, y, w, h), pts, b in arrows:
        sv = SVG(w, h, T, 'Arrow to the next station of the loop.')
        sv.add(f'<rect x="0" y="0" width="{w}" height="{h}" fill="none"/>')  # gives the sketch filter a box
        sv.arrow(pts, col)
        out.append(sv.render(x, y, bi(b)))
    inner = (H2('We attack our own monitors to find lower bounds on safety', T) + ''.join(out)
             + FOOT('19', 'loc-arena', T)
             + NOTES('Loop as specified for this slide in the deck manifest. '
                     'Main and side tasks, happened versus caught: loc-arena README and course. '
                     'Human and automated red teamers: project overview, Red Teaming in the Wild. '
                     'Sync and async monitors: loc-arena course, Monitoring page.'))
    return SECTION('red-team-loop', T, inner)


# ---------------------------------------------------------------- 20 closing
def s_closing(T):
    sv = SVG(640, 640, T, 'QR code linking to github.com/SreeSharvesh/loc-arena.', sketch=False)
    qr(sv, 0, 0, 640, LOC_MATRIX)
    inner = (PANEL(128, 112, 1232, 112, T, T['deep'])
             + MONO(FIRST + '/', 166, 141, 1160, T, utext(T), 600)
             + P('Our capacity to control AI systems will be critical to making AI go well, and [speaker to finish]',
                 128, 290, 960, T, 72, 700, lh=1.1, extra='; letter-spacing:-1.5px')
             + sv.render(1152, 270)
             + MONO(LOC_SHORT, 128, 742, 990, T, T['text'], size=48)
             + P('[team and mentors: names to confirm]', 128, 840, 960, T, 40, 500, T['muted'])
             + f'<p style="position:absolute; right:128px; bottom:64px; width:1400px; font-family:{FONT_M}; '
               f'font-size:28px; line-height:1; color:{T["muted"]}; text-align:right">{KURZ}</p>'
             + NOTES('Callback to the board’s first message (METR 2026). Takeaway and credits are placeholders '
                     'for the speaker. QR: version 3, error level M, links to ' + LOC_URL + '.'))
    return SECTION('closing', T, inner, radial(T))


SLIDES = [('one-agent', s_one_agent), ('swarms', s_swarms), ('hidden-channels', s_hidden),
          ('flag-game', s_flag), ('loc-arena', s_loc), ('red-team-loop', s_loop), ('closing', s_closing)]

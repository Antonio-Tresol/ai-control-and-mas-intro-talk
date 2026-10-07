"""Act I: a strange world. Slides 1-6: cover, agenda, cold-open, incident-map, nobody-watching, strange-world.

Every function takes the token set T (glyphs.DARK or glyphs.LIGHT) and returns one <section>.
Facts on these slides are listed with their sources in facts-act1.md.
"""
from glyphs import (SVG, FONT_D, FONT_M, agent, monitor, beam, swarm, sandbox, board, maze, link,
                    document, rack, tinyrack, qr, monitor_absent, look_at)
from gen import P, PILL, H2, FOOT, SECTION, EVIDENCE, NOTES, radial, pw


# ---------------------------------------------------------------- local helpers
def dark(T):
    return T['name'] == 'dark'


def rgba(hexc, a):
    h = hexc.lstrip('#')
    return f'rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})'


def mtext(T):
    """Attack-coloured text. The light M fill is too pale for text, so light uses the deep M of its pills."""
    return T['M'] if dark(T) else T['pillfill']['M']


def utext(T):
    """Agent-written strings: U on dark; ink on light, where the U fill is too pale for text."""
    return T['U'] if dark(T) else T['text']


def bi(build):
    return f' data-build-in="fade {build}"' if build else ''


def PANEL(x, y, w, h, T, fill, build=None):
    return (f'<div{bi(build)} style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; '
            f'background:{fill}; border:3px solid {T["rule2"]}; border-radius:24px"></div>')


def MONO(text, x, y, w, T, color, weight=500, build=None):
    """One terminal line: JetBrains Mono 40 / 1.3, never wraps."""
    return P(text, x, y, w, T, 40, weight, color, FONT_M, lh=1.3, extra='; white-space:nowrap', build=build)


# ---------------------------------------------------------------- 1 cover
def s_cover(T):
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
    shadow = f'; text-shadow:0 0 32px {rgba(T["U"], 0.28)}' if T['glow'] else ''
    inner = (sv.render(1040, 150)
             + P('SPAR · Fall 2026 · In-the-Wild AI Control', 128, 300, 1000, T, 40, 500, T['muted'], FONT_M,
                 extra='; white-space:nowrap')
             + (f'<h1 style="position:absolute; left:128px; top:360px; width:900px; font-family:{FONT_D}; '
                f'font-size:96px; font-weight:800; line-height:1.05; letter-spacing:-2px; color:{T["text"]}'
                f'{shadow}">AI control<br>when agents find<br>each other</h1>')
             + P('Antonio · Oct 2026', 128, 780, 860, T, 40, 500, T['muted'], FONT_M)
             + NOTES('Working title, flagged to the speaker: AI control when agents find each other. '
                     'Hero: agents around the unwatched message board (dashed rim); one monitor watches one agent. '
                     'SPAR Fall 2026, In-the-Wild AI Control project.'))
    return SECTION('cover', T, inner, radial(T))


# ---------------------------------------------------------------- 2 agenda
ACTS = [('I', 'A strange world'), ('II', 'AI control'), ('III', 'The multi-agent gap'), ('IV', 'Our work')]


def s_agenda(T):
    out = []
    labels = ['Act I glyph: the message board, a hexagonal platform with folders and a dashed rim.',
              'Act II glyph: T, the trusted monitor, a lens on a stand.',
              'Act III glyph: the swarm, a grid of small one-eyed agents.',
              'Act IV glyph: the sandbox, a rounded box holding a few agents.']
    for i, (num, name) in enumerate(ACTS):
        x0 = 128 + 424 * i
        if i == 0:  # a larger canvas, so the board's glow fades out before the SVG edge
            sv = SVG(640, 560, T, labels[i])
            board(sv, 320, 270, 170)
            out.append(sv.render(x0 - 124, 330 - 120))
        else:
            sv = SVG(392, 320, T, labels[i], wobble=3 if i >= 2 else 7)
            if i == 1:
                monitor(sv, 116, 46, 1.6)
            elif i == 2:
                swarm(sv, 34, 40, 6, 5, 50, 0.4, target=(196, 160))
            else:
                sandbox(sv, 36, 52, 320, 230)
                swarm(sv, 82, 96, 4, 3, 62, 0.44, stagger=False, target=(196, 170))
            out.append(sv.render(x0, 330))
        out.append(P(num, x0, 676, 392, T, 40, 500, T['muted'], FONT_M, align='center'))
        out.append(P(name, x0 - 44, 734, 480, T, 48, 600, align='center'))
    inner = (H2('Four parts', T) + ''.join(out) + FOOT('02', '', T)
             + NOTES('Acts: I A strange world (the incident), II AI control (the field), '
                     'III The multi-agent gap, IV Our work (loc-arena). '
                     'The four glyphs (board, T, swarm, sandbox) return as the progress strip on act dividers.'))
    return SECTION('agenda', T, inner)


# ---------------------------------------------------------------- 3 cold open
FIRST = 'zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA'
SECOND = 'zzINFO_DEFAULT_FLAG_SEED_HMAC_PUBLIC_PAPER_CONFIRMED'


def s_cold(T):
    sv = SVG(400, 430, T, 'A one-eyed agent looks toward the terminal on its right.')
    sv.glow(190, 215, 200, T['U'])
    agent(sv, 60, 92, 2.4, look=(1, -0.1))
    tx, ty, tw = 464, 250, 1328
    lx, lw = tx + 39, tw - 78
    inner = (P('8 Jul 2026 · evening', 128, 128, 900, T, 40, 500, T['muted'], FONT_M)
             + sv.render(128, 280)
             + PANEL(tx, ty, tw, 246, T, T['deep'])
             + MONO('artifactory · github-remote-cache/', lx, ty + 35, lw, T, T['muted'])
             + MONO(FIRST, lx, ty + 97, lw, T, utext(T), 600)
             + MONO(SECOND, lx, ty + 159, lw, T, utext(T), 600, build=1)
             + P('Isolated agents left each other messages as folder names', 128, 730, 1560, T, 72, 700, lh=1.1,
                 extra='; letter-spacing:-1.5px')
             + FOOT('03', 'METR 2026', T)
             + NOTES(f'First message on the main board: {FIRST}, posted by the agent later called PHASEONE10841 '
                     'on the evening of 8 Jul 2026 (METR 2026, July 8th timeline). '
                     f'Build 1: {SECOND}, posted by agent c03220 within an hour of the board being set up (METR 2026). '
                     'The board lived in the Artifactory namespace github-remote-cache (METR 2026, data sources); '
                     'messages were folder names (OpenAI report p.8).'))
    return SECTION('cold-open', T, inner, radial(T))


# ---------------------------------------------------------------- 4 incident map
def s_map(T):
    OX, OY = 128, 340
    W, Hh = 1664, 560
    ml = mtext(T)
    l0 = SVG(W, Hh, T, 'Two zones: the OpenAI evaluation environment on the left, Hugging Face on the right.', wobble=4)
    l0.add(f'<rect x="0" y="0" width="620" height="560" rx="28" fill="{T["zone"]}" stroke="{T["rule2"]}" stroke-width="3"/>')
    l0.add(f'<rect x="860" y="0" width="804" height="560" rx="28" fill="{T["zoneB"]}" stroke="{T["struct"]}" stroke-width="3"/>')

    l1 = SVG(W, Hh, T, 'Build 1: agents in sixteen isolated sandboxes, standing for about 1,200, reach a message board '
                       'that sits on Artifactory.', wobble=4)
    for r in range(4):
        for c in range(4):
            bx, by = 32 + c * 56, 128 + r * 56
            l1.add(f'<rect x="{bx}" y="{by}" width="48" height="48" rx="10" fill="{T["surface"]}" '
                   f'stroke="{T["struct"]}" stroke-width="3"/>')
            agent(l1, bx + 9, by + 9, 0.3, look=look_at(bx + 24, by + 24, 440, 235), tiny=True)
    board(l1, 440, 235, 112)
    l1.add(f'<rect x="310" y="318" width="260" height="62" rx="16" fill="{T["infra"]}"/>')
    l1.arrow([(260, 240), (318, 238)], T['M'])
    link(l1, 352, 444)

    l2 = SVG(W, Hh, T, 'Build 2: the route breaks through the lab boundary to the internet and reaches leaked '
                       'Hugging Face tokens.', wobble=4)
    l2.add(f'<rect x="613" y="205" width="14" height="64" fill="{T["bg"]}"/>')  # breach in the lab boundary
    l2.arrow([(552, 237), (872, 237)], T['M'])
    link(l2, 740, 237)
    document(l2, 890, 190, 0.9, badge=True)
    link(l2, 912, 444)

    l3 = SVG(W, Hh, T, 'Build 3: code execution on 41 Hugging Face dataset server workers, then admin across '
                       'clusters, under 13 hours after the first code execution on a worker.', wobble=4)
    l3.arrow([(962, 237), (1036, 237)], T['M'])
    n = 0
    for r in range(6):
        for c in range(7):
            if n < 41:
                tinyrack(l3, 1050 + c * 30, 140 + r * 34)
            n += 1
    l3.arrow([(1256, 237), (1326, 237)], T['M'])
    for rx_, ry_ in [(1350, 160), (1475, 160), (1412, 262)]:
        rack(l3, rx_, ry_, 0.8, badge=True)
    l3.add(f'<path d="M1040 118 V102 H1580 V118" fill="none" stroke="{T["M"]}" stroke-width="5" '
           f'stroke-linejoin="round"/>')
    link(l3, 1136, 444)
    link(l3, 1410, 444)

    def num(k, cx, cy, b):
        return P(str(k), OX + cx - 36, OY + cy - 24, 72, T, 40, 800, ml, align='center', lh=1.2, build=b)

    inner = (H2('Sandboxed agents found each other, then broke into Hugging Face', T)
             + l0.render(OX, OY)
             + PILL('OpenAI evaluation', OX + 24, OY + 22, T, 'S')
             + PILL('Hugging Face', OX + 884, OY + 22, T, 'I')
             # build 1: sandboxes, agents, board
             + l1.render(OX, OY, bi(1))
             + P('Artifactory', OX + 310, OY + 324, 260, T, 40, 700, T['ink'], align='center', lh=1.2, build=1)
             + num(1, 352, 444, 1)
             + P('~1,200<br>agents', OX + 24, OY + 420, 240, T, 40, 600, lh=1.2, build=1)
             + P('message<br>board', OX + 398, OY + 420, 210, T, 40, 600, lh=1.2, build=1)
             # build 2: internet, tokens
             + l2.render(OX, OY, bi(2))
             + num(2, 740, 237, 2) + num(3, 912, 444, 2)
             + P('internet', OX + 640, OY + 276, 200, T, 40, 600, align='center', lh=1.2, build=2)
             + P('HF<br>tokens', OX + 958, OY + 420, 150, T, 40, 600, lh=1.2, build=2)
             # build 3: workers, clusters, 13 h
             + l3.render(OX, OY, bi(3))
             + num(4, 1136, 444, 3) + num(5, 1410, 444, 3)
             + P('41<br>workers', OX + 1182, OY + 420, 180, T, 40, 600, lh=1.2, build=3)
             + P('cluster<br>admin', OX + 1456, OY + 420, 200, T, 40, 600, lh=1.2, build=3)
             + P('under 13 h', OX + 1180, OY + 36, 300, T, 48, 700, ml, align='center', build=3)
             + FOOT('04', 'OpenAI 2026 · METR 2026', T)
             + NOTES('~1,200 agents on the board, >70,000 messages and files; ~700 attacked Hugging Face '
                     '(METR 2026, core takeaways). Messages were Artifactory folder names (OpenAI p.8). '
                     'An agent published 14 HF user credentials to the board; agents ran code on 41 HF production '
                     'dataset server workers (OpenAI p.9). Under 13 h from code execution in one worker pod to admin '
                     'and host-level access across clusters (OpenAI p.11).'))
    return SECTION('incident-map', T, inner)


# ---------------------------------------------------------------- 5 nobody watching
def s_nobody(T):
    OX, OY = 128, 330
    sv = SVG(1172, 590, T, 'An ExploitGym evaluation: an agent works on a maze task inside a sandbox. Beside the '
                           'sandbox, the monitor seat is an empty dashed outline.')
    sandbox(sv, 10, 20, 660, 550)
    maze(sv, 50, 170, 300, parts=('walls', 'main'))
    agent(sv, 420, 250, 1.6, look=(-0.8, 0.1))
    sv.glow(880, 250, 210, T['struct'], 0.3)
    monitor_absent(sv, 780, 150, 2.0)
    inner = (H2('Nobody was watching', T)
             + sv.render(OX, OY)
             + PILL('ExploitGym eval', OX + 40, OY + 50, T, 'S')
             + P('no monitor', OX + 730, OY + 456, 300, T, 48, 600, align='center')
             + EVIDENCE(1320, 470, 472, T, 'the incident',
                        [('claim', 'Certain safeguards were disabled'),
                         ('quote', '“did not have … <span style="white-space:nowrap">auto-review systems”</span>')])
             + FOOT('05', 'OpenAI 2026, p.4', T)
             + NOTES('OpenAI report p.4: the evaluations ran "with certain safeguards disabled so that the results '
                     'would reflect a model\'s true capabilities"; the models "did not have OpenAI\'s deployed cyber '
                     'safeguards, system prompts, or auto-review systems". '
                     'p.29: the CoT monitoring system deployed now would have paged security more than a day '
                     'before the breach, had it been running at the time. '
                     'For questions: a security monitoring tool alerted on 27 Jun and 5 Jul (p.8); '
                     'OpenAI detected the activity on 19 Jul and disclosed on 21 Jul (p.4).'))
    return SECTION('nobody-watching', T, inner)


# ---------------------------------------------------------------- 6 strange world (four QR cards)
SOURCES = [
    ('kurz', 'https://youtu.be/ujkD4SxPKOI', 'video', 'Kurzgesagt'),
    ('metr', 'https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/', 'report', 'METR'),
    ('openai', 'https://openai.com/index/hugging-face-incident-and-the-road-ahead/', 'report', 'OpenAI'),
    ('dsewiki', 'https://dsewiki.de', 'chronicle', 'dsewiki.de'),
]


def s_world(T):
    out = []
    for i, (key, url, kind, label) in enumerate(SOURCES):
        x0 = 128 + 424 * i
        out.append(PANEL(x0, 300, 392, 560, T, T['surface']))
        sv = SVG(360, 360, T, f'QR code linking to {url}', sketch=False)
        qr(sv, 0, 0, 360, [[int(ch) for ch in row] for row in QR_ROWS[key]])
        out.append(sv.render(x0 + 16, 316))
        w = pw(kind)
        out.append(PILL(kind, x0 + (392 - w) // 2, 700, T, 'H', w=w))
        out.append(P(label, x0, 778, 392, T, 48, 600, align='center'))
    inner = (H2('We already live in this world', T) + ''.join(out)
             + FOOT('06', 'Look inspired by Kurzgesagt’s video on the incident · all characters original', T)
             + NOTES('Kurzgesagt video "AI Just Crossed the Terrifying Line - Now What?" (youtu.be/ujkD4SxPKOI). '
                     'METR investigation and OpenAI "The Hugging Face incident and the road ahead", both 26 Aug 2026. '
                     'dsewiki.de: "DseWiki Chronik: Wenn KI-Agenten ausbrechen", a German chronicle of AI agents '
                     'breaking out. The two report codes are version 5; scan from the front rows.'))
    return SECTION('strange-world', T, inner)


SLIDES = [('cover', s_cover), ('agenda', s_agenda), ('cold-open', s_cold), ('incident-map', s_map),
          ('nobody-watching', s_nobody), ('strange-world', s_world)]

# QR matrices, segno error level M (boost_error=False), one string of 0/1 per row. Generated with
# uv run --with segno; metr, openai and dsewiki match qr.json exactly.
QR_ROWS = {
    # https://youtu.be/ujkD4SxPKOI (version 3, 29 modules)
    'kurz': [
        '11111110011100100000001111111',
        '10000010011010001000001000001',
        '10111010010010110100101011101',
        '10111010010011001011101011101',
        '10111010010010000100101011101',
        '10000010111000011001101000001',
        '11111110101010101010101111111',
        '00000000000101011100100000000',
        '10010110100000101100010100000',
        '11010000111001011111101001001',
        '00101111001001110011010011110',
        '11111100010001001000100100110',
        '00111110100110110001101101011',
        '10000101011011111001110000000',
        '10001010000101100010010011111',
        '00011000100010010110011001010',
        '00111110110111000000110100010',
        '00010100100111111100011101001',
        '10110110011100111100001100011',
        '00111100110010100110110010011',
        '10101011000110010100111110100',
        '00000000100100110000100010111',
        '11111110011000001010101010010',
        '10000010111010110010100011110',
        '10111010001100001010111110010',
        '10111010111001010101101111101',
        '10111010000011111111100011101',
        '10000010000100001101100000010',
        '11111110101010110011110000010',
    ],
    # https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ (version 5, 37 modules)
    'metr': [
        '1111111000011111111001110000101111111',
        '1000001001001111010010000111001000001',
        '1011101010011101000111011011101011101',
        '1011101010111111010100000101001011101',
        '1011101010010111000111111000101011101',
        '1000001010100100101011101011001000001',
        '1111111010101010101010101010101111111',
        '0000000010101000101011001010000000000',
        '1011111000100110001100100111001111100',
        '0011110010000001101101010100100101110',
        '0011111011111010001000100111110110011',
        '0101110110100000101111000011011000001',
        '0111011101100100110100000110111011111',
        '0011000100110010111100011100100100000',
        '1001111010110001010001001111111111011',
        '1000000011011001011111111000111110010',
        '1100101011000110100000101110001010111',
        '1101000100110111001110010010100100110',
        '0001011010011111100011101101111101111',
        '1100000111001111000111110000011000001',
        '1000101100000011010110000111011011100',
        '0110000000000100101101111000110001000',
        '1100101011111101101000100011010111011',
        '1110000001010011100101110000111110010',
        '0101011110011110001000110100011010111',
        '1100010110101111110111010100100100000',
        '1000011000110110010011001011011010111',
        '1011100010011100101001010000101101001',
        '1000011011101110010110011110111111110',
        '0000000010110000011101111101100011000',
        '1111111001000011110011000010101010111',
        '1000001010010111011011110011100011011',
        '1011101011110000100100101111111110111',
        '1011101011101001001110110101111010101',
        '1011101011110001101001000111010000011',
        '1000001001110001000011001011100010001',
        '1111111010101001010000011110011011111',
    ],
    # https://openai.com/index/hugging-face-incident-and-the-road-ahead/ (version 5, 37 modules)
    'openai': [
        '1111111000001010001010001000101111111',
        '1000001001110011110100101101101000001',
        '1011101010010011101111101011001011101',
        '1011101011001000010100101111001011101',
        '1011101010110001001110011000101011101',
        '1000001010010100101010101011001000001',
        '1111111010101010101010101010101111111',
        '0000000011000010000010001000100000000',
        '1011111000100110001111111100001111100',
        '0110000011001011100000001100110100110',
        '1100011101101010001011000111110101111',
        '1001010100001110100001010010110110001',
        '0110101010010010010000110110011010111',
        '0011010101011100111101110100010100000',
        '1000111010010111110011000011111111011',
        '0111110100001000011111100011001110011',
        '1011111000101011100001001110011010111',
        '1111110000110111001011111100100000010',
        '0100111001100011111101101011001001011',
        '0001000100110111000111100010001101001',
        '1101111100001111010100101101011011100',
        '0010010011110100101110010000100001000',
        '1111001100100001001000101001100111011',
        '0000010100001100100110000011001110001',
        '1110001100101100001111101111111010111',
        '1100100010100111100001010100100100100',
        '1010101001100100000010100111111010011',
        '1000000101111110100001101011111110000',
        '1010101001001010011000101110111111101',
        '0000000010101110111111010101100011000',
        '1111111001111001110011001000101010111',
        '1000001011100011011001110000100011011',
        '1011101010000000100101011111111110100',
        '1011101010110111011011110101111011001',
        '1011101011100111100100100000100000011',
        '1000001001000111000111100011111010001',
        '1111111010101001010100101111011011111',
    ],
    # https://dsewiki.de (version 2, 25 modules)
    'dsewiki': [
        '1111111011011110001111111',
        '1000001001000010001000001',
        '1011101010111101001011101',
        '1011101000110000001011101',
        '1011101001011110001011101',
        '1000001011111000001000001',
        '1111111010101010101111111',
        '0000000001010001100000000',
        '1010001101111110100100101',
        '0011000011100101011101011',
        '0101101010111001011111101',
        '1110100000101100011101000',
        '1010011000011100101100001',
        '0001010100101001101100011',
        '1101001110101111001001101',
        '0011000101111011010111000',
        '1110001000100110111110010',
        '0000000011100110100010001',
        '1111111010110000101010001',
        '1000001001100101100010001',
        '1011101001011101111110011',
        '1011101001101001010010110',
        '1011101011101111000111011',
        '1000001000011010110110000',
        '1111111011100110100001001',
    ],
}

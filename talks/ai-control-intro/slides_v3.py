"""Three slide edits, applied to saved copies of both published decks (read them fresh first).

1. threats: cards shortened; a build-step chain below them ends in loss of control
   (International AI Safety Report, Jan 2025, §2.2.3). Sector icons are original drawings.
2. strange-world: opens on the Kurzgesagt thumbnail; [click] brings up the four QR cards over it.
3. closing: the repeated sparai.org line is gone, the QR is smaller, and orange agents
   roam along the top of the folder-name board (an <x-embed>, CSS animation only).

usage: python3 slides_v3.py <EN deck root> <ES deck root> <EN thumb blob> <ES thumb blob>
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHARS = os.path.join(HERE, '..', '..', 'assets', 'characters', 'v2', 'svg', 'on-dark')
RED, INK, DIM, LINE = '#FF3B5C', '#ECE8FF', '#A3AADB', '#8A93C9'

T = {
    'en': dict(
        n1='Escapes oversight', n2='Gains compute and access', n3='Loss of control',
        a1='Build 1: lines from all three failure cards merge into one chain. First link: an attacking agent beside the dashed outline of a missing monitor. It escapes oversight.',
        a2='Build 2: second link: copies of the agent on two server racks, next to a key. It gains compute and access.',
        a3='Build 3: last link, framed in red: seven critical systems, each with the attack badge: finance, transport, communication, logistics, health, energy and defense. Loss of control.',
        cite='Shlegeris 2024 · Greenblatt 2025 · OpenAI 2026, p.14 · Intl AI Safety Report 2025',
        notes='\nBuilds 1–3: any of the three can start a chain: the AI escapes oversight, gains compute and access, and the chain ends in loss of control: “one or more general-purpose AI systems come to operate outside of anyone’s control, with no clear path to regaining control” (International AI Safety Report, Jan 2025, §2.2.3; the report says expert views on its likelihood vary greatly). Sector icons follow the sectors named in Kurzgesagt’s video; the drawings are original.\nThe July incident reached the first two links: no monitor ran (OpenAI p.4), agents reached the internet and Hugging Face (p.8–9), ran code on 41 production workers (p.9) and reached admin access across several clusters in under 13 h (p.11), plus a privileged pod in OpenAI’s own cluster (p.14).',
        alt='Thumbnail of Kurzgesagt’s video: a huge red eye under the words WE LOST CONTROL.',
        foot='Thumbnail © Kurzgesagt – In a Nutshell · all other art original',
        sw_notes='Opens on the thumbnail of Kurzgesagt’s video (credited in the footer); [click] brings up the four codes over it. ',
        pill='SPAR project page',
        close_notes=' Orange agents roam along the top of the board (a live embed; exports show one still frame).',
    ),
    'es': dict(
        n1='Escapa de la supervisión', n2='Gana cómputo y accesos', n3='Pérdida de control',
        a1='Paso 1: líneas desde las tres tarjetas de fallas se unen en una sola cadena. Primer eslabón: un agente atacante junto al contorno punteado de un monitor ausente. Escapa de la supervisión.',
        a2='Paso 2: segundo eslabón: copias del agente sobre dos racks de servidores, junto a una llave. Gana cómputo y accesos.',
        a3='Paso 3: último eslabón, enmarcado en rojo: siete sistemas críticos, cada uno con la insignia de ataque: finanzas, transporte, comunicaciones, logística, salud, energía y defensa. Pérdida de control.',
        cite='Shlegeris 2024 · Greenblatt 2025 · OpenAI 2026, p.14 · Intl AI Safety Report 2025',
        notes='\nPasos 1–3: cualquiera de las tres puede iniciar una cadena: la IA escapa de la supervisión, gana cómputo y accesos, y la cadena termina en pérdida de control: escenarios en que uno o más sistemas de IA de propósito general pasan a operar fuera del control de cualquier persona, sin un camino claro para recuperarlo (International AI Safety Report, enero de 2025, §2.2.3; el informe dice que las opiniones de especialistas sobre su probabilidad varían mucho). Los íconos de sectores siguen los que nombra el video de Kurzgesagt; los dibujos son propios.\nEl incidente de julio llegó a los dos primeros eslabones: no corrió ningún monitor (OpenAI p.4), los agentes llegaron a internet y a Hugging Face (p.8–9), ejecutaron código en 41 servidores de producción (p.9) y en menos de 13 h obtuvieron acceso de administrador en varios clústeres (p.11), además de un pod privilegiado en el propio clúster de OpenAI (p.14).',
        alt='Miniatura del video de Kurzgesagt: un enorme ojo rojo bajo las palabras WE LOST CONTROL.',
        foot='Miniatura © Kurzgesagt – In a Nutshell · el resto del arte es propio',
        sw_notes='Abre con la miniatura del video de Kurzgesagt (crédito en el pie); [clic] muestra los cuatro códigos encima. ',
        pill='Proyecto en SPAR',
        close_notes=' Agentes naranjas recorren la parte superior del tablero (un embed animado; las exportaciones muestran un cuadro fijo).',
    ),
}


def sub1(pat, rep, s, n=1, flags=0):
    s2, k = re.subn(pat, rep, s, flags=flags)
    assert k == n, (pat[:70], k, n)
    return s2


def circ(cx, cy, r):
    return f'M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 '


# ---------- 1. threats ----------

AGENT_ATTACK = ('<path d="M0 34h12v9H0z M88 34h12v9H88z M0 54h12v9H0z M88 54h12v9H88z M28 84h12v18H28z M60 84h12v18H60z" fill="#B87708"/>'
                '<rect x="8" y="6" width="84" height="84" rx="28" fill="#F4AB1A"/><ellipse cx="30" cy="21" rx="11" ry="6" fill="#FFD98A"/>'
                '<circle cx="50" cy="48" r="24" fill="#0B1026"/><circle cx="59" cy="48.9" r="12" fill="#FF3B5C"/>'
                '<path d="M86 -8 L102 8 L86 24 L70 8 Z" fill="#FF3B5C" stroke="#0B1026" stroke-width="5" stroke-linejoin="round"/>')
AGENT_SMALL = ('<path d="M28 84h12v18H28z M60 84h12v18H60z" fill="#B87708"/><rect x="8" y="6" width="84" height="84" rx="28" fill="#F4AB1A"/>'
               '<circle cx="50" cy="48" r="24" fill="#0B1026"/><circle cx="53" cy="48.9" r="12" fill="#FDFBFF"/>')


def rack(x, y):
    units = ' '.join(f'M{x} {y + i * 23}h72v19H{x}z' for i in range(3))
    leds = ' '.join(f'M{x + 8} {y + 8 + i * 23}h5v4h-5z M{x + 22} {y + 8 + i * 23}h40v4H{x + 22}z' for i in range(3))
    return f'<path d="{units}" fill="{DIM}"/><path d="{leds}" fill="#0B1026"/>'


def sectors(x0, y0):
    """Seven 56px sector icons in a row: finance, transport, communication, logistics, health, energy, defense."""
    out, badges = [], []
    for i in range(7):
        x = x0 + i * 68
        g = lambda d, fill=INK, extra='': f'<path transform="translate({x} {y0})" d="{d}" fill="{fill}"{extra}/>'
        if i == 0:  # bank
            out.append(g('M4 20 L28 5 L52 20 Z M8 24h9v20H8z M23.5 24h9v20h-9z M39 24h9v20h-9z M4 47h48v7H4z'))
        elif i == 1:  # plane
            out.append(f'<path transform="translate({x} {y0}) rotate(45 28 28)" d="M28 2 C31 2 32.5 6 32.5 10 L32.5 21 L54 33 L54 39 L32.5 32 L32.5 44 L40 50 L40 54 L28 51 L16 54 L16 50 L23.5 44 L23.5 32 L2 39 L2 33 L23.5 21 L23.5 10 C23.5 6 25 2 28 2 Z" fill="{INK}"/>')
        elif i == 2:  # chat bubbles
            out.append(g('M8 4h26a6 6 0 0 1 6 6v14a6 6 0 0 1 -6 6H18l-8 8v-8H8a6 6 0 0 1 -6 -6V10a6 6 0 0 1 6 -6z'))
            out.append(g('M24 24h24a6 6 0 0 1 6 6v10a6 6 0 0 1 -6 6h-2v8l-8 -8H24a6 6 0 0 1 -6 -6V30a6 6 0 0 1 6 -6z', DIM, ' stroke="#2A0F24" stroke-width="3"'))
        elif i == 3:  # logistics network
            out.append(g('M28 28 L28 7 M28 28 L48 20 M28 28 L43 47 M28 28 L13 47 M28 28 L8 20', 'none', f' stroke="{INK}" stroke-width="4" stroke-linecap="round"'))
            out.append(g(circ(28, 28, 9) + circ(28, 7, 6) + circ(48, 20, 6) + circ(43, 47, 6) + circ(13, 47, 6) + circ(8, 20, 6)))
        elif i == 4:  # health cross
            out.append(g('M21 4h14v17h17v14H35v17H21V35H4V21h17z'))
        elif i == 5:  # energy bolt
            out.append(g('M33 2 L9 32 H26 L21 54 L47 21 H30 Z'))
        else:  # defense shield
            out.append(g('M28 3 L50 11 V27 C50 41 40 50 28 54 C16 50 6 41 6 27 V11 Z'))
            out.append(g('M28 11 L43 16.5 V27 C43 37 36.5 43.5 28 46.5 Z', DIM))
        bx, by = x + 52, y0 - 2
        badges.append(f'M{bx} {by - 9} L{bx + 9} {by} L{bx} {by + 9} L{bx - 9} {by} Z')
    out.append(f'<path d="{" ".join(badges)}" fill="{RED}" stroke="#2A0F24" stroke-width="3" stroke-linejoin="round"/>')
    return ''.join(out)


def marker(mid):
    return (f'<defs><marker id="{mid}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible">'
            f'<path d="M0 0 L4 2 L0 4 Z" fill="{RED}"/></marker></defs>')


def chain(t):
    svg = lambda aria, body, k: (f'<svg width="1664" height="220" viewBox="0 0 1664 220" role="img" aria-label="{aria}" '
                                 f'style="position:absolute; left:128px; top:700px" data-build-in="fade {k}">{body}</svg>')
    red = f'stroke="{RED}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    s1 = (marker('threatsx4i1') + f'<path d="M832 0 L832 22 M1404 0 L1404 22 L260 22" {red}/>'
          f'<path d="M260 0 L260 44" {red} marker-end="url(#threatsx4i1)"/>'
          f'<g transform="translate(220 66) scale(0.8)">{AGENT_ATTACK}</g>'
          f'<path d="{circ(368, 98, 30)}M368 128 V146 M350 150 H386" fill="none" stroke="{LINE}" stroke-width="4" stroke-dasharray="8 7" stroke-linecap="round"/>')
    s2 = (marker('threatsx5i1') + f'<path d="M424 104 L688 104" {red} marker-end="url(#threatsx5i1)"/>'
          + rack(724, 92) + rack(812, 92)
          + f'<g transform="translate(737 47) scale(0.45)">{AGENT_SMALL}</g><g transform="translate(825 47) scale(0.45)">{AGENT_SMALL}</g>'
          f'<path d="{circ(918, 104, 14)}M932 104 H962 M952 104 V116 M962 104 V114" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    s3 = (marker('threatsx6i1') + f'<path d="M990 104 L1128 104" {red} marker-end="url(#threatsx6i1)"/>'
          f'<rect x="1152" y="40" width="504" height="164" rx="24" fill="none" stroke="{RED}" stroke-width="18" opacity="0.18"/>'
          f'<rect x="1152" y="40" width="504" height="164" rx="24" fill="#2A0F24" stroke="{RED}" stroke-width="4"/>'
          + sectors(1172, 60))
    lab = lambda left, top, w, size, weight, color, text, k: (
        f'<p data-build-in="fade {k}" style="position:absolute; left:{left}px; top:{top}px; width:{w}px; font-family:\'Outfit\', \'Trebuchet MS\', sans-serif; '
        f'font-size:{size}px; font-weight:{weight}; line-height:1.15; color:{color}; text-align:center">{text}</p>')
    return (svg(t['a1'], s1, 1) + lab(128, 862, 520, 40, 600, '#F2F0FF', t['n1'], 1)
            + svg(t['a2'], s2, 2) + lab(700, 862, 520, 40, 600, '#F2F0FF', t['n2'], 2)
            + svg(t['a3'], s3, 3) + lab(1280, 840, 504, 48, 700, RED, t['n3'], 3))


def threats(s, t):
    s = sub1(r'top:330px; width:520px; height:584px;', 'top:256px; width:520px; height:444px;', s, 3)

    def shrink(m):
        attrs, left, inner = m.group(1), int(m.group(2)), m.group(3)
        return (f'<svg width="390" height="225" viewBox="0 0 390 225"{attrs}style="position:absolute; left:{left + 65}px; top:268px">'
                f'<g transform="scale(0.75)">{inner}</g></svg>')
    s = sub1(r'<svg width="520" height="300" viewBox="0 0 520 300"([^>]*?)style="position:absolute; left:(\d+)px; top:344px">(.*?)</svg>',
             shrink, s, 3, re.S)
    s = sub1(r'top:664px; width:464px;', 'top:506px; width:464px;', s, 3)
    s = sub1(r'left:148px; top:806px;', 'left:148px; top:620px;', s)
    s = sub1(r'>Shlegeris 2024 · Greenblatt 2025 · OpenAI 2026, p\.14<', '>' + t['cite'] + '<', s)
    s = sub1(r'(<p style="position:absolute; left:128px; bottom:64px;)', lambda m: chain(t) + m.group(1), s)
    s = sub1(r'</aside>', lambda m: t['notes'] + '</aside>', s)
    return s


# ---------- 2. strange-world ----------

def strange_world(s, t, blob):
    img = (f'<img src="{blob}" alt="{t["alt"]}" style="position:absolute; left:400px; top:300px; width:1120px; height:549px; '
           f'object-fit:cover; border-radius:24px; box-shadow:0 0 96px rgba(255,59,92,0.45)">'
           '<div data-build-in="fade 1" style="position:absolute; left:128px; top:252px; width:1664px; height:640px; '
           'background:rgba(11,16,38,0.72); border-radius:24px"></div>')
    s = sub1(r'(</h2>)', lambda m: m.group(1) + img, s)
    s = sub1(r'<div style="position:absolute; left:(\d+)px; top:300px; width:392px; height:560px; background:#151C3D;',
             lambda m: f'<div data-build-in="fade 1" style="position:absolute; left:{m.group(1)}px; top:300px; width:392px; height:560px; '
                       'background:rgba(21,28,61,0.8); backdrop-filter:blur(16px);', s, 4)
    s = sub1(r'(<svg width="360" height="360" viewBox="0 0 360 360" )', r'\1data-build-in="fade 1" ', s, 4)
    s = sub1(r'<p style="(position:absolute; left:\d+px; top:(?:700|778)px;)', r'<p data-build-in="fade 1" style="\1', s, 8)
    s = sub1(r'(text-align:right">)[^<]*(</p>)', lambda m: m.group(1) + t['foot'] + m.group(2), s)
    s = sub1(r'<aside>', '<aside>' + t['sw_notes'], s)
    return s


# ---------- 3. closing ----------

def agent_inner(name):
    svg = open(os.path.join(CHARS, name + '.svg'), encoding='utf-8').read()
    return re.search(r'(<g transform="translate\(20 32\)">.*</g>)</svg>', svg, re.S).group(1)


def embed():
    walkers = [  # shape, start, end (px), period (s), phase (s)
        ('agent-chip-purple', 110, 430, 15, -3), ('agent-round-teal', 300, 700, 19, -3.6),
        ('agent-tall-green', 560, 900, 14, -2.4), ('agent-round-coral', 760, 1080, 21, -16.6),
        ('agent-hex-yellow', 940, 1150, 12, -4.8), ('rogue-glitch-drop', 360, 600, 17, -0.3),
    ]
    css = (':root{color-scheme:dark}html{background:#0b1026 radial-gradient(ellipse at 50% 42%,#18225a 0%,#0b1026 58%,#070a1a 100%) -128px -12px/1920px 1080px no-repeat}html,body{margin:0;height:100%;overflow:hidden}body{background:transparent}'
           '.w{position:absolute;bottom:0;left:0;width:72px;height:76px;animation:m var(--d) linear var(--o) infinite}'
           '.f{width:100%;height:100%;animation:f var(--d) steps(1,end) var(--o) infinite}'
           '.b{display:block;width:100%;height:100%;animation:b .45s ease-in-out infinite alternate}'
           '.g .b{animation-duration:1.4s}.r{width:92px}.r .b{animation-duration:.9s}'
           '@keyframes m{0%,100%{transform:translateX(var(--a))}42%,50%{transform:translateX(var(--z))}92%{transform:translateX(var(--a))}}'
           '@keyframes f{0%{transform:scaleX(1)}46%{transform:scaleX(-1)}96%{transform:scaleX(1)}}'
           '@keyframes b{to{transform:translateY(-6px)}}'
           '.gx{animation:j 1.7s steps(1,end) infinite}'
           '@keyframes j{0%,20%,64%,100%{transform:translate(0,0)}8%{transform:translate(-4px,1px)}13%{transform:translate(3px,-1px)}58%{transform:translate(4px,0)}}'
           '.c{animation:c 1.7s steps(1,end) infinite}@keyframes c{0%,20%,64%,100%{transform:translate(-6px,0)}8%{transform:translate(-13px,0)}58%{transform:translate(-10px,2px)}}'
           '.m{animation:n 1.7s steps(1,end) infinite}@keyframes n{0%,20%,64%,100%{transform:translate(6px,0)}8%{transform:translate(13px,0)}58%{transform:translate(10px,-2px)}}'
           '.s{animation:s 1.7s steps(1,end) infinite}@keyframes s{0%,20%,64%,100%{opacity:1}8%{opacity:0}58%{opacity:.25}}'
           '@media (prefers-reduced-motion:reduce){*{animation:none!important}}')
    vb = 'viewBox="14 20 112 118"'
    first = agent_inner('agent-chip-orange').replace('cx="53.2" cy="48.9"', 'cx="54" cy="55"')  # the first agent, looking down at its folder name
    figs = [f'<div class="w" style="animation:none;transform:translateX(18px)"><div class="f" style="animation:none">'
            f'<svg class="b" style="animation:none" {vb}>{first}</svg></div></div>']
    for name, a, z, d, o in walkers:
        cls = 'w g' if 'ghost' in name else 'w'
        inner = agent_inner(name)
        if name.startswith('rogue-glitch'):  # RGB split layers jitter, glitch slices flicker
            inner = inner.replace('<g transform="translate(-6 0)"', '<g class="c"').replace('<g transform="translate(6 0)"', '<g class="m"')
            inner = re.sub(r'<rect ([^>]*(?:stroke="none"|width="[67]" height="[67]")[^>]*)/>', r'<rect class="s" \1/>', inner)
            inner = inner.replace('<g transform="translate(20 32)">', '<g transform="translate(20 32)"><g class="gx">', 1)[:-4] + '</g></g>'
        figs.append(f'<div class="{cls}" style="--a:{a}px;--z:{z}px;--d:{d}s;--o:{o}s"><div class="f"><svg class="b" {vb}>{inner}</svg></div></div>')
    figs.append(f'<div class="w r" style="--a:820px;--z:1120px;--d:27s;--o:-7.2s"><div class="f"><svg class="b" viewBox="14 20 132 118">'
                f'{agent_inner("monitor-robot-scanning")}</svg></div></div>')
    html = f'<style>{css}</style>' + ''.join(figs)
    return f'<x-embed style="position:absolute; left:128px; top:12px; width:1232px; height:100px">{html}</x-embed>'


def closing(s, t, lang):
    s = sub1(r'<p style="position:absolute; top:\d+px; left:128px; width:1000px; font-family:\'JetBrains Mono\'[^>]*>sparai\.org · In-the-Wild AI Control</p>', '', s)
    s = sub1(r'(<p style="position:absolute; top:)556(px; left:128px; width:)', r'\g<1>576\2', s)
    q = {'en': 768, 'es': 792}[lang]
    s = sub1(r'top:\d+px; left:128px; width:140px; height:140px', f'top:{q}px; left:128px; width:140px; height:140px', s)
    s = sub1(r'top:\d+px; left:290px;([^>]*>(?:About me|Sobre mí)<)', f'top:{q + 12}px; left:290px;\\1', s)
    s = sub1(r'top:\d+px; left:290px;([^>]*>antonio-tresol)', f'top:{q + 64}px; left:290px;\\1', s)
    s = sub1(r'top:240px; left:1192px; width:600px;([^>]*>)[^<]*</p>', f'top:256px; left:1272px; width:520px;\\1{t["pill"]}</p>', s)
    s = sub1(r'style="position:absolute; top:312px; left:1192px; width:600px; height:600px"', 'style="position:absolute; top:332px; left:1272px; width:520px; height:520px"', s)
    s = sub1(r'(zzHELP_PHASEONE_ARV010841_NO_CONSUMER_SEEK_IDEA/</p>)', lambda m: m.group(1) + embed(), s)
    s = sub1(r'</aside>', t['close_notes'] + '</aside>', s)
    return s


if __name__ == '__main__':
    en_root, es_root, en_blob, es_blob = sys.argv[1:5]
    for root, lang, blob in ((en_root, 'en', en_blob), (es_root, 'es', es_blob)):
        t = T[lang]
        for sid, fn in (('threats', lambda s: threats(s, t)), ('strange-world', lambda s: strange_world(s, t, blob)),
                        ('closing', lambda s: closing(s, t, lang))):
            p = os.path.join(root, 'project', 'slides', sid + '.html')
            s = fn(open(p, encoding='utf-8').read())
            open(p, 'w', encoding='utf-8').write(s)
            n = len(re.findall(r'<(?!/)(?!x-embed)[a-zA-Z]', re.sub(r'<x-embed.*?</x-embed>', '<x-embed></x-embed>', s, flags=re.S)))
            svgs = [len(m.encode()) for m in re.findall(r'<svg.*?</svg>', re.sub(r'<x-embed.*?</x-embed>', '', s, flags=re.S), re.S)]
            emb = re.search(r'<x-embed.*?</x-embed>', s, re.S)
            print(f'{lang} {sid}: {n} elements, largest svg {max(svgs)} B' + (f', embed {len(emb.group(0).encode())} B' if emb else ''))

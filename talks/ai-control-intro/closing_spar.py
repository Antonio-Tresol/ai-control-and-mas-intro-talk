"""Closing slide: QR to the SPAR project page instead of the repo, plus a credits line (mentors named, team described)."""
import re
import sys

import segno

URL = 'https://sparai.org/projects/f26/rec8RybPH2kNV6qDa'
SHORT = 'sparai.org/projects/f26/rec8RybPH2kNV6qDa'
TEXT = {
    'en': dict(pill='SPAR project page', mentors='Mentors: Sree Sharvesh and Thao Pham',
               team='5 mentees, mostly AI software engineers and security engineers',
               aria='QR code linking to the In-the-Wild AI Control project page on sparai.org.',
               notes='Callback to the board’s first message (METR 2026). Big QR: links to ' + URL + ' (the SPAR project page). '
                     'Credits: mentors Sree Sharvesh and Thao Pham; five mentees, mostly software engineers working with AI, and security engineers. '
                     'Small QR: links to https://antonio-tresol.github.io/ (the speaker’s page).'),
    'es': dict(pill='Página del proyecto en SPAR', mentors='Mentores: Sree Sharvesh y Thao Pham',
               team='5 mentees, en su mayoría ingenieros de software en IA e ingenieros de seguridad',
               aria='Código QR que enlaza a la página del proyecto In-the-Wild AI Control en sparai.org.',
               notes='Referencia al primer mensaje del tablero (METR 2026). QR grande: enlaza a ' + URL + ' (la página del proyecto en SPAR). '
                     'Créditos: mentores Sree Sharvesh y Thao Pham; cinco mentees, en su mayoría ingenieros de software que trabajan con IA, e ingenieros de seguridad. '
                     'QR pequeño: enlaza a https://antonio-tresol.github.io/ (la página del expositor).'),
}


def qr_svg(aria, size=600, quiet=4):
    q = segno.make(URL, error='m', boost_error=False)
    m = [[1 if c else 0 for c in row] for row in q.matrix]
    n = len(m)
    u = size / (n + 2 * quiet)
    d = []
    for r, row in enumerate(m):
        c = 0
        while c < n:
            if row[c]:
                s = c
                while c < n and row[c]:
                    c += 1
                d.append(f'M{(s+quiet)*u:.2f} {(r+quiet)*u:.2f}h{(c-s)*u:.2f}v{u:.2f}h-{(c-s)*u:.2f}z')
            else:
                c += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" aria-label="{aria}" '
            f'style="position:absolute; top:312px; left:1192px; width:{size}px; height:{size}px">'
            f'<rect x="0" y="0" width="{size}" height="{size}" rx="16" fill="#FDFBFF"/>'
            f'<path d="{"".join(d)}" fill="#0B1026" shape-rendering="crispEdges"/></svg>'), q.version


def rewrite(path, lang):
    t = TEXT[lang]
    s = open(path, encoding='utf-8').read()
    big, version = qr_svg(t['aria'])
    pill = (f'<p style="position:absolute; top:240px; left:1192px; width:600px; padding:6px 22px; border-radius:999px; background:#1C2550; '
            f'color:#F2F0FF; font-family:Outfit, \'Trebuchet MS\', sans-serif; font-size:40px; font-weight:700; line-height:1.15; text-align:center; white-space:nowrap">{t["pill"]}</p>')
    s, n1 = re.subn(r'<svg [^>]*viewBox="0 0 640 640"[^>]*>.*?</svg>', lambda m: pill + big, s, count=1, flags=re.S)
    s, n2 = re.subn(r'style="position:absolute; top:756px; left:128px; width:150px; height:150px"',
                    'style="position:absolute; top:776px; left:128px; width:140px; height:140px"', s)
    s, n3 = re.subn(r'<p style="position:absolute; top:774px; left:300px;', '<p style="position:absolute; top:788px; left:290px;', s)
    s, n4 = re.subn(r'<p style="position:absolute; top:826px; left:300px;', '<p style="position:absolute; top:840px; left:290px;', s)
    url_p = (f'<p style="position:absolute; top:716px; left:128px; width:1000px; font-family:\'JetBrains Mono\', \'Courier New\', monospace; '
             f'font-size:40px; font-weight:500; line-height:1.3; white-space:nowrap; color:#f2f0ff">{SHORT}</p>')
    s, n5 = re.subn(r'<p style="position:absolute; top:590px; left:128px;[^>]*>github\.com/SreeSharvesh/loc-arena</p>', url_p, s)
    credits = (f'<p style="position:absolute; top:552px; left:128px; width:1000px; font-family:Outfit, \'Trebuchet MS\', sans-serif; font-size:40px; '
               f'font-weight:500; line-height:1.15; color:#b8bee0"><span style="color:#F2F0FF">{t["mentors"]}</span><br>{t["team"]}</p>')
    s, n6 = re.subn(r'<p style="position:absolute; top:676px; left:128px;[^>]*>\[[^\]]*\]</p>', credits, s)
    s, n7 = re.subn(r'<aside>.*?</aside>', f'<aside>{t["notes"]}</aside>', s, flags=re.S)
    assert (n1, n2, n3, n4, n5, n6, n7) == (1, 1, 1, 1, 1, 1, 1), (n1, n2, n3, n4, n5, n6, n7)
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok, QR version', version)


rewrite(sys.argv[1], 'en')
rewrite(sys.argv[2], 'es')

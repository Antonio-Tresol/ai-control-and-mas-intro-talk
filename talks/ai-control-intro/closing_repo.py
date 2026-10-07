"""Closing slide: a second QR, to the talk repository, beside the SPAR project QR (both 320 px).

The repo URL is encoded as typed (byte mode, version 5 at level M): the upper-case alphanumeric
version is smaller but OpenCV's decoder failed on it, so the plain URL is the safer code.

usage: uv run --with segno python3 closing_repo.py <EN closing.html> <ES closing.html>
"""
import re
import sys

import segno

REPO = 'https://github.com/Antonio-Tresol/ai-control-and-mas-intro-talk'
TEXT = {
    'en': dict(spar='SPAR', repo='Repository',
               aria='QR code linking to the talk repository on GitHub: slide code, drawings, sources and scripts.',
               notes=' Second QR, right: links to ' + REPO + ' (the talk repository: slide code, drawings, sources.bib, draft scripts).'),
    'es': dict(spar='SPAR', repo='Repositorio',
               aria='Código QR que enlaza al repositorio de la charla en GitHub: código de las diapositivas, dibujos, fuentes y guiones.',
               notes=' Segundo QR, a la derecha: enlaza a ' + REPO + ' (el repositorio de la charla: código de las diapositivas, dibujos, sources.bib y guiones).'),
}
TOP, SIZE, X_SPAR, X_REPO = 452, 320, 1120, 1472


def pill(text, left):
    return (f'<p style="position:absolute; top:{TOP - 72}px; left:{left}px; width:{SIZE}px; padding:6px 22px; border-radius:999px; '
            f'background:#1C2550; color:#F2F0FF; font-family:Outfit, \'Trebuchet MS\', sans-serif; font-size:40px; font-weight:700; '
            f'line-height:1.15; text-align:center; white-space:nowrap">{text}</p>')


def qr_svg(aria, size=600, quiet=4):
    q = segno.make(REPO, error='m', boost_error=False)
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
                d.append(f'M{(s + quiet) * u:.2f} {(r + quiet) * u:.2f}h{(c - s) * u:.2f}v{u:.2f}h-{(c - s) * u:.2f}z')
            else:
                c += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" aria-label="{aria}" '
            f'style="position:absolute; top:{TOP}px; left:{X_REPO}px; width:{SIZE}px; height:{SIZE}px">'
            f'<rect x="0" y="0" width="{size}" height="{size}" rx="16" fill="#FDFBFF"/>'
            f'<path d="{"".join(d)}" fill="#0B1026" shape-rendering="crispEdges"/></svg>'), q.version, q.mode


def requr(path, lang):
    """Swap an existing repo QR for a freshly encoded one (same position and size)."""
    t = TEXT[lang]
    s = open(path, encoding='utf-8').read()
    s, n = re.subn(r'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-label="' + re.escape(t['aria'])
                   + r'".*?</svg>', lambda m: qr_svg(t['aria'])[0], s, flags=re.S)
    assert n == 1, n
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'repo QR re-encoded, version', qr_svg('')[1], qr_svg('')[2])


def rewrite(path, lang):
    t = TEXT[lang]
    s = open(path, encoding='utf-8').read()
    s, n1 = re.subn(r'<p style="position:absolute; top:256px; left:1272px; width:520px;[^>]*>[^<]*</p>',
                    lambda m: pill(t['spar'], X_SPAR) + pill(t['repo'], X_REPO), s)
    s, n2 = re.subn(r'(<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"[^>]*?)'
                    r'style="position:absolute; top:332px; left:1272px; width:520px; height:520px">(.*?</svg>)',
                    lambda m: (m.group(1) + f'style="position:absolute; top:{TOP}px; left:{X_SPAR}px; width:{SIZE}px; '
                               f'height:{SIZE}px">' + m.group(2) + qr_svg(t['aria'])[0]), s, flags=re.S)
    s, n3 = re.subn(r'</aside>', lambda m: t['notes'] + '</aside>', s)
    assert (n1, n2, n3) == (1, 1, 1), (n1, n2, n3)
    open(path, 'w', encoding='utf-8').write(s)
    _, version, mode = qr_svg('')
    print(lang, 'ok, repo QR version', version, mode)


if __name__ == '__main__':
    fn = requr if '--requr' in sys.argv else rewrite
    args = [a for a in sys.argv[1:] if a != '--requr']
    fn(args[0], 'en')
    fn(args[1], 'es')

# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Slide 6 without dsewiki: the thumbnail stays visible (left, with the video's code under it);
METR and OpenAI codes on the right. The click brings up the three code cards.

usage: uv run strange_world_n.py <slide file> <en|es>
"""
import re
import sys

path, lang = sys.argv[1], sys.argv[2]
s = open(path, encoding='utf-8').read()
FONT = "font-family:'Outfit', 'Trebuchet MS', sans-serif"
L = {'en': dict(report='report', notes_old='dsewiki.de: "DseWiki Chronik: Wenn KI-Agenten ausbrechen", a German chronicle of AI agents breaking out. ',
                click='[click] brings up the four codes over it.', click_new='[click] brings up the three codes beside it.'),
     'es': dict(report='informe', notes_old='dsewiki.de: "DseWiki Chronik: Wenn KI-Agenten ausbrechen", una crónica en alemán sobre agentes de IA que se escapan. ',
                click='[clic] muestra los cuatro códigos encima.', click_new='[clic] muestra los tres códigos al lado.')}[lang]

section = re.match(r'<section[^>]*>', s).group(0)
h2 = re.search(r'<h2.*?</h2>', s, re.S).group(0)
img = re.search(r'<img [^>]*>', s).group(0)
blob = re.search(r'src="(/_blob/[0-9a-f]+)"', img).group(1)
alt = re.search(r'alt="([^"]*)"', img).group(1)


def qr(host):
    m = re.search(r'<svg width="360" height="360" viewBox="0 0 360 360"[^>]*aria-label="[^"]*' + re.escape(host) + r'[^"]*"[^>]*>(.*?)</svg>', s, re.S)
    aria = re.search(r'aria-label="([^"]*)"', m.group(0)).group(1)
    return aria, m.group(1)


footers = re.findall(r'<p style="position:absolute; (?:left:128px|right:128px); bottom:64px;.*?</p>', s, re.S)
aside = re.search(r'<aside>.*?</aside>', s, re.S).group(0)
assert len(footers) == 2 and L['notes_old'] in aside and L['click'] in aside, (len(footers),)
aside = aside.replace(L['notes_old'], '').replace(L['click'], L['click_new'])


def card(left, top, w, h):
    return (f'<div data-build-in="fade 1" style="position:absolute; left:{left}px; top:{top}px; width:{w}px; height:{h}px; '
            'background:#151C3D; border:3px solid #3A4478; border-radius:24px"></div>')


def code(host, left, top, size):
    aria, inner = qr(host)
    return (f'<svg width="360" height="360" viewBox="0 0 360 360" data-build-in="fade 1" role="img" aria-label="{aria}" '
            f'style="position:absolute; left:{left}px; top:{top}px; width:{size}px; height:{size}px">{inner}</svg>')


def pill(left, top, w, text):
    return (f'<p data-build-in="fade 1" style="position:absolute; left:{left}px; top:{top}px; width:{w}px; padding:6px 22px; border-radius:999px; '
            f'background:#ECE8FF; color:#0B1026; {FONT}; font-size:40px; font-weight:700; line-height:1.15; text-align:center; white-space:nowrap">{text}</p>')


def name(left, top, text):
    return (f'<p data-build-in="fade 1" style="position:absolute; left:{left}px; top:{top}px; width:460px; {FONT}; font-size:48px; '
            f'font-weight:600; line-height:1.15; color:#F2F0FF; text-align:left">{text}</p>')


pw = {'video': 162, 'report': 184, 'informe': 208}
body = (h2
        + f'<img src="{blob}" alt="{alt}" style="position:absolute; left:128px; top:268px; width:816px; height:400px; object-fit:cover; '
          'border-radius:24px; box-shadow:0 0 80px rgba(255,59,92,0.45)">'
        # left: the video's code under its thumbnail
        + card(128, 692, 816, 228) + code('youtu.be', 142, 706, 200) + pill(370, 728, pw['video'], 'video') + name(370, 806, 'Kurzgesagt')
        # right: the two reports
        + card(976, 268, 816, 316) + code('metr.org', 990, 282, 288) + pill(1310, 352, pw[L['report']], L['report']) + name(1310, 430, 'METR')
        + card(976, 604, 816, 316) + code('openai.com', 990, 618, 288) + pill(1310, 688, pw[L['report']], L['report']) + name(1310, 766, 'OpenAI'))
out = section + body + ''.join(footers) + aside + '</section>'
open(path, 'w', encoding='utf-8').write(out)
print(lang, 'ok', len(re.findall(r'<(?!/)[a-zA-Z]', out)), 'elements')

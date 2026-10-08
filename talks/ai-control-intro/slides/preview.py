# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Render one deck's slide files into a single preview page.

usage: uv run preview.py en|es      -> preview-<lang>.html next to this file
       open preview-en.html?solo=N   -> slide N alone at 1920x1080 (for screenshots)

Each slide is one <section> in the Slides artifact format, listed in <lang>/project/deck.json.
Live <x-embed> blocks (the animated cover and the closing slide's message strip) become iframes, so
their own <style> stays inside them instead of restyling every slide on the page.
Images stored as /_blob/... uploads (the Kurzgesagt thumbnail and logo) are not in this repository
and show as empty boxes.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = ('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap')
EMBED = re.compile(r'<x-embed style="([^"]*)">(.*?)</x-embed>', re.S)


def isolate_embeds(sec):
    return EMBED.sub(lambda m: f'<iframe style="{m.group(1)}; border:0" scrolling="no" '
                               f'srcdoc="{html.escape(m.group(2))}"></iframe>', sec)


def main(lang):
    root = os.path.join(HERE, lang, 'project')
    order = json.load(open(os.path.join(root, 'deck.json'), encoding='utf-8'))['order']
    frames = []
    for n, sid in enumerate(order, 1):
        sec = isolate_embeds(open(os.path.join(root, 'slides', f'{sid}.html'), encoding='utf-8').read())
        frames.append(f'<div class="slot" id="slot{n}"><div class="frame">{sec}</div><p class="cap">{n:02d} {sid}</p></div>')
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Preview ({lang})</title>
<link rel="stylesheet" href="{FONTS}">
<style>
body{{margin:0;background:#222;font-family:sans-serif}}
.slot{{width:960px;margin:24px auto}}
.frame{{width:960px;height:540px;overflow:hidden;position:relative}}
.frame section{{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;transform-origin:0 0;transform:scale(.5)}}
.frame section *{{margin:0;box-sizing:border-box}}
.frame section aside{{display:none}}
.cap{{color:#aaa;font:14px monospace}}
body.solo .slot{{display:none;margin:0;width:1920px}}
body.solo .slot.show{{display:block}}
body.solo .frame{{width:1920px;height:1080px}}
body.solo .frame section{{transform:none}}
body.solo .cap{{display:none}}
</style></head><body>
{''.join(frames)}
<script>
var q=new URLSearchParams(location.search),solo=q.get('solo');
if(solo){{document.body.classList.add('solo');var el=document.getElementById('slot'+solo);if(el)el.classList.add('show');}}
</script></body></html>'''
    out = os.path.join(HERE, f'preview-{lang}.html')
    open(out, 'w', encoding='utf-8').write(page)
    print('wrote', out, len(order), 'slides')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'en')

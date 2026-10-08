# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Assemble the deck's slide files into one preview page.

Usage: uv run preview.py            -> out/preview.html with every slide in order.json
       open out/preview.html?solo=N  -> slide N alone at 1920x1080 (for headless screenshots)

Slides live in out/project/slides/<id>.html, one <section> each, exactly as the Slides artifact
type stores them. Missing slides show as an empty placeholder frame.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
SLIDES = os.path.join(OUT, 'project', 'slides')
FONTS = ('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@400;500;600&display=swap')


def main():
    order = json.load(open(os.path.join(HERE, 'order.json')))
    frames = []
    for n, sid in enumerate(order, 1):
        path = os.path.join(SLIDES, f'{sid}.html')
        if os.path.exists(path):
            sec = open(path, encoding='utf-8').read()
        else:
            sec = (f'<section id="{sid}" style="background:#333; padding:128px">'
                   f'<p style="font-size:72px; color:#fff">missing: {sid}</p></section>')
        frames.append(f'<div class="slot" id="slot{n}"><div class="frame">{sec}</div>'
                      f'<p class="cap">{n:02d} {sid}</p></div>')
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Deck preview</title>
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
var q=new URLSearchParams(location.search),solo=q.get('solo'),step=q.get('step');
if(solo){{document.body.classList.add('solo');var el=document.getElementById('slot'+solo);if(el)el.classList.add('show');
 if(step!==null){{el.querySelectorAll('[data-build-in]').forEach(function(b){{var k=+((b.getAttribute('data-build-in').match(/\\d+/)||[0])[0]);if(k>+step)b.style.opacity='0';}});}}}}
</script></body></html>'''
    open(os.path.join(OUT, 'preview.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.join(OUT, 'preview.html'), len(order), 'slides')


if __name__ == '__main__':
    main()

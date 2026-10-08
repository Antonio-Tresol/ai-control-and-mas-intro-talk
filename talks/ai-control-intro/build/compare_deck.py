# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""The whole deck in dark sketch and dark clean, side by side. Writes ../compare-deck.html."""
import json
import os
import re

import glyphs
import gen
import act1
import act2
import act34

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'compare-deck.html')
order = json.load(open(os.path.join(HERE, 'order.json')))
fns = dict(act1.SLIDES + act2.SLIDES + act34.SLIDES)


def render(sketch):
    glyphs.SKETCH_DEFAULT = sketch
    gen.DARK = glyphs.DARK
    out = []
    for sid in order:
        glyphs.begin_slide(sid + ('s' if sketch else 'c'))
        html = fns[sid](glyphs.DARK)
        out.append(re.sub(r'<aside>.*?</aside>', '', html, flags=re.S))
    return out


cols = {'sketch': render(True), 'clean': render(False)}
rows = ''.join(
    f'<section class="row"><h2>{i + 1:02d} · {sid}</h2><div class="grid">'
    + ''.join(f'<figure data-v="{k}"><figcaption>Dark · {k}</figcaption><div class="frame">{cols[k][i]}</div></figure>'
              for k in ('sketch', 'clean'))
    + '</div></section>'
    for i, sid in enumerate(order))
page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Sketch or clean</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>
body{{margin:0;background:#4a4a4f;color:#f4f4f4;font-family:'Outfit',sans-serif}}
header{{padding:24px 32px}} header h1{{margin:0 0 6px;font-size:28px}} header p{{margin:0;font-size:16px;opacity:.85}}
.bar{{display:flex;gap:8px;margin-top:14px}} .bar button{{font:inherit;font-size:15px;padding:6px 14px;border-radius:8px;border:1px solid #888;background:#3c3c40;color:#fff;cursor:pointer}} .bar button.on{{background:#fff;color:#111}}
.row{{padding:8px 32px 24px}} .row>h2{{font-size:18px;margin:8px 0 10px;font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(2,800px);gap:18px}}
figure{{margin:0}} figcaption{{font-family:'JetBrains Mono',monospace;font-size:14px;margin-bottom:6px}}
.frame{{width:800px;height:450px;overflow:hidden;position:relative;border-radius:6px}}
.frame>section{{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;transform-origin:0 0;transform:scale(.41667)}}
.frame section *{{margin:0;box-sizing:border-box}}
body.one .grid{{grid-template-columns:1600px}} body.one figure{{display:none}} body.one figure.pick{{display:block}}
body.one .frame{{width:1600px;height:900px}} body.one .frame>section{{transform:scale(.83333)}}
</style></head><body>
<header><h1>The deck, dark: sketch or clean?</h1>
<p>All 20 slides with every build step shown. Numbers and text are identical; only the drawing style differs. QR codes stay clean in both.</p>
<div class="bar"><button class="on" data-k="all">Side by side</button><button data-k="sketch">Sketch only</button><button data-k="clean">Clean only</button></div></header>
{rows}
<script>
document.querySelectorAll('.bar button').forEach(function(b){{b.onclick=function(){{
 document.querySelectorAll('.bar button').forEach(function(x){{x.classList.toggle('on',x===b)}});
 var k=b.dataset.k; document.body.classList.toggle('one',k!=='all');
 document.querySelectorAll('figure').forEach(function(f){{f.classList.toggle('pick',f.dataset.v===k)}});}}}});
</script></body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', os.path.normpath(OUT), len(page))

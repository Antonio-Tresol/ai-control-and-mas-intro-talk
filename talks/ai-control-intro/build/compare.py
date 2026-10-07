"""Render the specimen slides in four looks for the speaker to choose from:
clean or sketch drawings, dark or light palette. Writes ../compare.html."""
import os
import glyphs
import gen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'compare.html')
DARK_TOKENS, LIGHT_TOKENS = glyphs.DARK, glyphs.LIGHT
RADIAL_DARK = gen.RADIAL
RADIAL_LIGHT = 'radial-gradient(ellipse at 50% 42%, #FFFDF8 0%, #F6F3ED 58%, #EEE9DF 100%)'
SLIDES = [gen.s_cold, gen.s_cover, gen.s_cast, gen.s_map, gen.s_bignum, gen.s_game,
          gen.s_multiples, gen.s_qr, gen.s_project]
VARIANTS = [('dark-clean', 'Dark · clean', False, False), ('dark-sketch', 'Dark · sketch', False, True),
            ('light-clean', 'Light · clean', True, False), ('light-sketch', 'Light · sketch', True, True)]


def render(light, sketch):
    gen.DARK = LIGHT_TOKENS if light else DARK_TOKENS
    gen.RADIAL = RADIAL_LIGHT if light else RADIAL_DARK
    glyphs.SKETCH_DEFAULT = sketch
    return [f()[0] for f in SLIDES]


cols = {key: render(light, sketch) for key, _, light, sketch in VARIANTS}
rows = []
for i, f in enumerate(SLIDES):
    cells = ''.join(
        f'<figure data-v="{key}"><figcaption>{label}</figcaption><div class="frame">{cols[key][i]}</div></figure>'
        for key, label, _, _ in VARIANTS)
    rows.append(f'<section class="row"><h2>{i + 1:02d} · {f.__name__[2:]}</h2><div class="grid">{cells}</div></section>')

page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Look comparison</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>
body{{margin:0;background:#5a5a5e;color:#f4f4f4;font-family:'Outfit',sans-serif}}
header{{padding:24px 32px}} header h1{{margin:0 0 6px;font-size:28px}} header p{{margin:0;font-size:16px;opacity:.85}}
.bar{{display:flex;gap:8px;margin-top:14px}} .bar button{{font:inherit;font-size:15px;padding:6px 14px;border-radius:8px;border:1px solid #888;background:#3c3c40;color:#fff;cursor:pointer}} .bar button.on{{background:#fff;color:#111}}
.row{{padding:8px 32px 28px}} .row>h2{{font-size:18px;margin:8px 0 10px;font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(2,800px);gap:18px}}
figure{{margin:0}} figcaption{{font-family:'JetBrains Mono',monospace;font-size:14px;margin-bottom:6px}}
.frame{{width:800px;height:450px;overflow:hidden;position:relative;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,.35)}}
.frame>section{{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;transform-origin:0 0;transform:scale(.41667)}}
.frame section *{{margin:0;box-sizing:border-box}}
body.one .grid{{grid-template-columns:1600px}} body.one figure{{display:none}} body.one figure.pick{{display:block}}
body.one .frame{{width:1600px;height:900px}} body.one .frame>section{{transform:scale(.83333)}}
</style></head><body>
<header><h1>Pick a look: clean or sketch, dark or light</h1>
<p>The same nine specimen slides in four versions. Placeholder copy; the real deck follows the outline. Buttons show one version large.</p>
<div class="bar"><button class="on" data-k="all">All four</button><button data-k="dark-clean">Dark · clean</button><button data-k="dark-sketch">Dark · sketch</button><button data-k="light-clean">Light · clean</button><button data-k="light-sketch">Light · sketch</button></div></header>
{''.join(rows)}
<script>
document.querySelectorAll('.bar button').forEach(function(b){{b.onclick=function(){{
 document.querySelectorAll('.bar button').forEach(function(x){{x.classList.toggle('on',x===b)}});
 var k=b.dataset.k; document.body.classList.toggle('one',k!=='all');
 document.querySelectorAll('figure').forEach(function(f){{f.classList.toggle('pick',f.dataset.v===k)}});}}}});
</script></body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', os.path.normpath(OUT), len(page))

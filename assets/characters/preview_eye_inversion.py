"""Side-by-side preview: current eye vs inverted eye (black outer eye, white inner disc).
Writes eye-inversion-preview.html. Does not change the asset pack."""
import make_characters as C

DARK_EYE = '#0B1026'
ORIG_EYE = C.eye


def eye_current(cx, cy, r, look=(0.35, 0.1), iris=C.IRIS):
    return ORIG_EYE(cx, cy, r, look, iris)


def eye_inverted(cx, cy, r, look=(0.35, 0.1), iris=None, pupil=False):
    ix, iy = cx + look[0] * r * 0.38, cy + look[1] * r * 0.38
    g = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{DARK_EYE}"/>'
         f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{r*0.5:.1f}" fill="{C.SCLERA}"/>')
    if pupil:
        g += f'<circle cx="{ix + r*0.08:.1f}" cy="{iy:.1f}" r="{r*0.16:.1f}" fill="{DARK_EYE}"/>'
    return g


def agent_with(eye_fn, shape, color):
    old = C.eye
    C.eye = lambda cx, cy, r, look=(0.35, 0.1), iris=C.IRIS: eye_fn(cx, cy, r, look)
    try:
        return C.agent_svg(shape, color)
    finally:
        C.eye = old


VARIANTS = [('Current', eye_current),
            ('Inverted: black eye, white centre', eye_inverted),
            ('Inverted, with a small dark pupil', lambda *a, **k: eye_inverted(*a, pupil=True, **k))]
PICKS = [('chip', 'orange'), ('round', 'teal'), ('tall', 'purple'), ('drop', 'pink'), ('hex', 'green'), ('ghost', 'coral'),
         ('chip', 'sky'), ('round', 'yellow')]


def row(eye_fn, outline):
    return ''.join(f'<div class="t">{C.wrap(agent_with(eye_fn, s, c), f"{c} {s}", outline)}</div>' for s, c in PICKS)


html = ['<!doctype html><html><head><meta charset="utf-8"><title>Eye inversion preview</title><style>'
        'body{margin:0;padding:22px 26px;background:#2b2d33;color:#eee;font-family:system-ui,sans-serif}'
        'h1{font-size:20px;margin:0 0 14px} h2{font-size:15px;margin:18px 0 8px;font-weight:600}'
        '.row{display:grid;grid-template-columns:repeat(8,1fr);gap:8px;padding:10px;border-radius:12px}'
        '.dark{background:#0B1026} .light{background:#F6F3ED} .t svg{width:100%;height:auto;display:block}</style></head><body>'
        '<h1>Agent eyes: current vs inverted</h1>']
for label, fn in VARIANTS:
    html.append(f'<h2>{label}</h2><div class="row dark">{row(fn, False)}</div>'
                f'<div class="row light" style="margin-top:8px">{row(fn, True)}</div>')
html.append('</body></html>')
open('eye-inversion-preview.html', 'w').write(''.join(html))
print('ok')

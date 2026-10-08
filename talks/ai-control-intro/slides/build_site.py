"""Build the GitHub Pages site: a full-screen viewer for each deck.

usage: python3 build_site.py <out dir>    -> <out>/index.html (English), <out>/es/index.html (Spanish)

The viewer steps through each slide's builds as the live deck does. Keys: → or Space forward,
← back, Home and End, G all slides, N speaker notes, F full screen, Esc closes a panel. The
address holds the slide number (#12), so a link can open one slide. Uses only the standard library.
"""
import json
import os
import re
import shutil
import sys

from preview import FONTS, HERE, isolate_embeds

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SITE = 'https://antonio-tresol.github.io/ai-control-and-mas-intro-talk/'
REPO = 'https://github.com/Antonio-Tresol/ai-control-and-mas-intro-talk'

UI = {
    'en': dict(
        dir='', up='', other='es/', other_lang='es', other_short='ES', other_name='Español',
        description='A 15-minute introduction to AI control and multi-agent systems, built around the '
                    'July 2026 OpenAI–Hugging Face incident. SPAR Fall 2026.',
        controls='Slide controls', prev='Previous', next='Next', grid='All slides', notes='Speaker notes',
        full='Full screen', source='Source on GitHub', close='Close', slide='Slide', of='of',
        help='← → or Space to move · G all slides · N notes · F full screen',
        noscript='This viewer needs JavaScript. The slide files are in the', repo='repository'),
    'es': dict(
        dir='es/', up='../', other='../', other_lang='en', other_short='EN', other_name='English',
        description='Una introducción de 15 minutos al control de IA y los sistemas multiagente, a partir '
                    'del incidente de OpenAI y Hugging Face de julio de 2026. SPAR, otoño de 2026.',
        controls='Controles de la presentación', prev='Anterior', next='Siguiente',
        grid='Todas las diapositivas', notes='Notas de la charla', full='Pantalla completa',
        source='Código en GitHub', close='Cerrar', slide='Diapositiva', of='de',
        help='← → o espacio para avanzar · G todas las diapositivas · N notas · F pantalla completa',
        noscript='Este visor necesita JavaScript. Los archivos de las diapositivas están en el',
        repo='repositorio'),
}

BLOB = re.compile(r'<img\b([^>]*\bsrc="/_blob/[^"]*"[^>]*)>')


def placeholder(m):
    """Uploaded images (the Kurzgesagt thumbnail and logo) are not ours to publish: show a dashed box."""
    attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    attrs.pop('src')
    alt, style = attrs.pop('alt', ''), attrs.pop('style', '')
    width = re.search(r'width:\s*(\d+)px', style)
    label = alt if width and int(width.group(1)) >= 300 else ''
    rest = ''.join(f' {k}="{v}"' for k, v in attrs.items())
    return (f'<div{rest} role="img" aria-label="{alt}" style="{style}; display:flex; align-items:center; '
            'justify-content:center; padding:40px; background:#10173a; border:3px dashed #3a4478; '
            "color:#b8bee0; font:500 34px/1.3 Outfit, 'Trebuchet MS', sans-serif; text-align:center\">"
            f'{label}</div>')


def icon(paths):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'


ICONS = dict(
    prev=icon('<path d="M15 18l-6-6 6-6"/>'),
    next=icon('<path d="M9 18l6-6-6-6"/>'),
    grid=icon('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
              '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
    notes=icon('<path d="M4 6h16M4 12h16M4 18h10"/>'),
    full=icon('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>'),
    source=icon('<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>'),
    close=icon('<path d="M6 6l12 12M18 6L6 18"/>'),
)

CSS = '''
:root{--bg:#05070f;--panel:rgba(11,16,38,.92);--ink:#f2f0ff;--muted:#b8bee0;--line:#2a3366;--accent:#f4ab1a;--focus:#a1d8ff}
html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);overflow:hidden;font-family:Outfit,'Trebuchet MS',sans-serif}
#stage{position:fixed;inset:0;touch-action:pan-y pinch-zoom;transition:right .25s ease,bottom .25s ease}
#deck{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform:translate(-50%,-50%) scale(var(--k,.5))}
#deck>section{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;opacity:0;visibility:hidden;transition:opacity .35s ease,visibility 0s linear .35s}
#deck>section.current{opacity:1;visibility:visible;transition:opacity .35s ease}
section *{margin:0;box-sizing:border-box}
section aside{display:none}
#deck [data-build-in]{opacity:0;transition:opacity .4s ease}
#deck iframe{pointer-events:none}
#deck [data-build-in].shown{opacity:1}
#bar{position:fixed;left:50%;bottom:16px;z-index:10;display:flex;align-items:center;gap:2px;padding:6px;transform:translateX(-50%);background:var(--panel);border:1px solid var(--line);border-radius:999px;box-shadow:0 8px 32px rgba(0,0,0,.45);backdrop-filter:blur(8px);transition:opacity .3s ease}
body.idle #bar{opacity:0;pointer-events:none}
body.idle{cursor:none}
#bar button,#bar a,#grid-close{display:inline-flex;align-items:center;justify-content:center;min-width:40px;height:40px;padding:0 10px;border:0;border-radius:999px;background:transparent;color:var(--ink);font:600 15px/1 Outfit,sans-serif;text-decoration:none;cursor:pointer}
#bar button:hover,#bar a:hover,#grid-close:hover{background:rgba(255,255,255,.08)}
#bar button:disabled{opacity:.35;cursor:default;background:transparent}
#bar button[aria-pressed=true]{background:rgba(161,216,255,.16);color:#a1d8ff}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
#bar svg,#grid-close svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
#count{min-width:76px;text-align:center;font:500 14px/1 'JetBrains Mono',monospace;color:var(--muted)}
.sep{width:1px;height:24px;margin:0 4px;background:var(--line)}
#progress{position:fixed;left:0;bottom:0;z-index:10;height:3px;background:var(--accent);transition:width .3s ease}
#notes{position:fixed;top:0;right:0;bottom:0;z-index:5;box-sizing:border-box;width:min(440px,40vw);padding:28px 28px 96px;overflow-y:auto;background:#0b1026;border-left:1px solid var(--line);transform:translateX(100%);visibility:hidden;transition:transform .25s ease,visibility 0s linear .25s}
body.notes-open #notes{transform:none;visibility:visible;transition:transform .25s ease}
body.notes-open #stage{right:min(440px,40vw)}
#notes h2{margin:0 0 6px;font:600 13px/1.2 'JetBrains Mono',monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
#notes h3{margin:0 0 16px;font:700 22px/1.25 Outfit,sans-serif}
#notes-text{margin:0;font:400 17px/1.55 Outfit,sans-serif;color:#dcdaf5;white-space:pre-line}
@media (max-width:760px){
#notes{top:auto;left:0;width:auto;height:46vh;border-left:0;border-top:1px solid var(--line);transform:translateY(100%)}
body.notes-open #stage{right:0;bottom:46vh}
#bar{bottom:10px;gap:0;padding:4px}
#bar button,#bar a{min-width:36px;padding:0 6px}
#count{min-width:60px}
}
@media (max-width:360px){#src,#bar .sep{display:none}}
#grid{position:fixed;inset:0;z-index:20;display:none;overflow-y:auto;padding:28px 24px 64px;background:rgba(5,7,15,.97)}
body.grid-open #grid{display:block}
#grid header{display:flex;align-items:center;gap:16px;max-width:1440px;margin:0 auto 20px}
#grid h1{margin:0;font:700 22px/1.2 Outfit,sans-serif}
#grid header p{flex:1;margin:0;font:500 13px/1.4 'JetBrains Mono',monospace;color:var(--muted)}
#grid ol{display:grid;grid-template-columns:repeat(auto-fill,minmax(256px,1fr));gap:20px;max-width:1440px;margin:0 auto;padding:0;list-style:none}
#grid ol button{display:block;width:100%;padding:0;border:0;background:none;color:var(--muted);text-align:left;cursor:pointer;font:500 13px/1.35 'JetBrains Mono',monospace}
.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;border:2px solid transparent;border-radius:10px;background:#0b1026}
#grid ol button.current .thumb{border-color:var(--accent)}
#grid ol button:hover .thumb{border-color:var(--line)}
.thumb section{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;transform-origin:0 0;transform:scale(var(--t,.13));pointer-events:none}
.cap{display:block;padding:8px 2px 0}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.noscript{position:fixed;inset:auto 0 40%;z-index:30;text-align:center;font:500 20px/1.5 Outfit,sans-serif}
.noscript a{color:var(--focus)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
'''

JS = '''
(() => {
  const ui = JSON.parse(document.getElementById('ui').textContent);
  const $ = id => document.getElementById(id);
  const body = document.body, stage = $('stage'), deck = $('deck');
  const slides = [...deck.children];
  const stepOf = el => parseInt((el.dataset.buildIn || '').split(' ')[1], 10) || 1;
  const steps = slides.map(s => [...new Set([...s.querySelectorAll('[data-build-in]')].map(stepOf))].sort((a, b) => a - b));
  const size = el => parseFloat(el.style.fontSize) || 0;
  const titleOf = s => {  // the heading, or the slide's largest line of text
    const el = s.querySelector('h1, h2') || [...s.querySelectorAll('p')].sort((a, b) => size(b) - size(a))[0];
    if (!el) return '';
    const copy = el.cloneNode(true);
    copy.querySelectorAll('br').forEach(br => br.replaceWith(' '));
    return copy.textContent.replace(/\\s+/g, ' ').trim();
  };
  let i = 0, k = 0;  // slide index; number of build steps shown

  const fit = () => {
    const r = stage.getBoundingClientRect();
    deck.style.setProperty('--k', Math.min(r.width / 1920, r.height / 1080));
  };

  function render(announce) {
    slides.forEach((s, n) => s.classList.toggle('current', n === i));
    const level = k ? steps[i][k - 1] : 0;
    slides[i].querySelectorAll('[data-build-in]').forEach(el => el.classList.toggle('shown', stepOf(el) <= level));
    $('count').textContent = `${i + 1} / ${slides.length}`;
    $('progress').style.width = `${(i + 1) / slides.length * 100}%`;
    $('prev').disabled = i === 0 && k === 0;
    $('next').disabled = i === slides.length - 1 && k === steps[i].length;
    const hash = `#${i + 1}`;
    if (location.hash !== hash) history.replaceState(null, '', hash);
    $('lang').href = ui.other + hash;
    const aside = slides[i].querySelector('aside');
    $('notes-title').textContent = `${i + 1}. ${titleOf(slides[i])}`;
    $('notes-text').textContent = aside ? aside.textContent.trim() : '';
    document.querySelectorAll('#grid-list button').forEach((b, n) => b.classList.toggle('current', n === i));
    if (announce) $('status').textContent = `${ui.slide} ${i + 1} ${ui.of} ${slides.length}: ${titleOf(slides[i])}`;
  }

  const go = n => { i = Math.max(0, Math.min(slides.length - 1, n)); k = steps[i].length; render(true); };
  const next = () => {
    const was = i;
    if (k < steps[i].length) k++; else if (i < slides.length - 1) { i++; k = 0; }
    render(i !== was);
  };
  const prev = () => {
    const was = i;
    if (k > 0) k--; else if (i > 0) { i--; k = steps[i].length; }
    render(i !== was);
  };
  const fromHash = () => parseInt(location.hash.slice(1), 10) || 1;

  function toggleNotes(open = !body.classList.contains('notes-open')) {
    body.classList.toggle('notes-open', open);
    $('notes').inert = !open;
    $('notes-btn').setAttribute('aria-pressed', open);
  }

  function buildGrid() {
    const list = $('grid-list');
    if (list.children.length) return;
    slides.forEach((s, n) => {
      const li = document.createElement('li'), b = document.createElement('button');
      const thumb = document.createElement('div'), cap = document.createElement('span');
      const copy = s.cloneNode(true);
      copy.classList.remove('current');
      copy.removeAttribute('id');
      copy.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));  // url(#…) resolves to the deck's copy
      thumb.className = 'thumb';
      thumb.appendChild(copy);
      cap.className = 'cap';
      cap.textContent = `${n + 1}. ${titleOf(s)}`;
      b.append(thumb, cap);
      b.addEventListener('click', () => { go(n); toggleGrid(false); });
      li.appendChild(b);
      list.appendChild(li);
    });
  }
  const sizeThumbs = () => document.querySelectorAll('.thumb').forEach(t => t.style.setProperty('--t', t.clientWidth / 1920));

  function toggleGrid(open = !body.classList.contains('grid-open')) {
    if (open) buildGrid();
    body.classList.toggle('grid-open', open);
    $('grid-btn').setAttribute('aria-pressed', open);
    if (open) {
      sizeThumbs();
      render(false);
      const cur = document.querySelector('#grid-list button.current');
      if (cur) { cur.focus(); cur.scrollIntoView({ block: 'center' }); }
    } else {
      $('grid-btn').focus();
    }
  }

  function toggleFull() {
    if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen();
  }

  $('prev').addEventListener('click', prev);
  $('next').addEventListener('click', next);
  $('grid-btn').addEventListener('click', () => toggleGrid());
  $('grid-close').addEventListener('click', () => toggleGrid(false));
  $('notes-btn').addEventListener('click', () => toggleNotes());
  if (document.fullscreenEnabled) {
    $('full-btn').addEventListener('click', toggleFull);
    document.addEventListener('fullscreenchange', () => $('full-btn').setAttribute('aria-pressed', !!document.fullscreenElement));
  } else {
    $('full-btn').hidden = true;
  }

  addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const grid = body.classList.contains('grid-open');
    const onControl = e.target.closest && e.target.closest('button, a');
    switch (e.key) {
      case 'Escape': if (grid) toggleGrid(false); else if (body.classList.contains('notes-open')) toggleNotes(false); return;
      case 'g': case 'G': toggleGrid(); return;
      case 'n': case 'N': if (!grid) toggleNotes(); return;
      case 'f': case 'F': if (document.fullscreenEnabled) toggleFull(); return;
    }
    if (grid) return;
    if ((e.key === ' ' || e.key === 'Enter') && onControl) return;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); (e.key === ' ' && e.shiftKey ? prev : next)(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { e.preventDefault(); i = 0; k = 0; render(true); }
    else if (e.key === 'End') { e.preventDefault(); go(slides.length - 1); }
  });

  let downX = null, downY = 0, swiped = false;
  stage.addEventListener('pointerdown', e => { downX = e.clientX; downY = e.clientY; });
  stage.addEventListener('pointerup', e => {
    if (downX === null) return;
    const dx = e.clientX - downX, dy = e.clientY - downY;
    downX = null;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) { swiped = true; (dx < 0 ? next : prev)(); }
  });
  stage.addEventListener('click', e => {
    if (swiped) { swiped = false; return; }
    const r = stage.getBoundingClientRect();
    (e.clientX - r.left < r.width / 3 ? prev : next)();
  });

  let idle;
  const wake = () => {
    body.classList.remove('idle');
    clearTimeout(idle);
    idle = setTimeout(() => {
      if (!body.classList.contains('grid-open') && !$('bar').matches(':hover, :focus-within')) body.classList.add('idle');
    }, 2500);
  };
  ['pointermove', 'pointerdown'].forEach(t => addEventListener(t, wake));
  addEventListener('keydown', e => { if (e.key === 'Tab') wake(); });

  new ResizeObserver(fit).observe(stage);
  addEventListener('resize', () => { if (body.classList.contains('grid-open')) sizeThumbs(); });
  addEventListener('hashchange', () => { if (fromHash() !== i + 1) go(fromHash() - 1); });

  fit();
  toggleNotes(false);
  go(fromHash() - 1);
  wake();
})();
'''

PAGE = '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}{dir}">
<link rel="alternate" hreflang="{lang}" href="{site}{dir}">
<link rel="alternate" hreflang="{other_lang}" href="{site}{other_dir}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{site}{dir}">
<meta property="og:image" content="{site}cover-{lang}.jpg">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="720">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#05070f">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>{css}</style>
</head>
<body>
<main id="stage" aria-label="{title}"><div id="deck">{sections}</div></main>
<nav id="bar" aria-label="{controls}">
<button id="prev" type="button" aria-label="{prev}" title="{prev} (←)">{icon_prev}</button>
<span id="count" aria-hidden="true"></span>
<button id="next" type="button" aria-label="{next}" title="{next} (→)">{icon_next}</button>
<span class="sep"></span>
<button id="grid-btn" type="button" aria-pressed="false" aria-label="{grid}" title="{grid} (G)">{icon_grid}</button>
<button id="notes-btn" type="button" aria-pressed="false" aria-label="{notes}" title="{notes} (N)">{icon_notes}</button>
<button id="full-btn" type="button" aria-pressed="false" aria-label="{full}" title="{full} (F)">{icon_full}</button>
<span class="sep"></span>
<a id="lang" href="{other}" hreflang="{other_lang}" lang="{other_lang}" aria-label="{other_name}" title="{other_name}">{other_short}</a>
<a id="src" href="{repo_url}" aria-label="{source}" title="{source}">{icon_source}</a>
</nav>
<div id="progress"></div>
<aside id="notes" aria-label="{notes}"><h2>{notes}</h2><h3 id="notes-title"></h3><p id="notes-text"></p></aside>
<div id="grid" role="dialog" aria-modal="true" aria-labelledby="grid-title">
<header><h1 id="grid-title">{title}</h1><p>{help}</p><button id="grid-close" type="button" aria-label="{close}" title="{close} (Esc)">{icon_close}</button></header>
<ol id="grid-list"></ol>
</div>
<p id="status" class="sr-only" aria-live="polite"></p>
<noscript><p class="noscript">{noscript} <a href="{repo_url}">{repo}</a>.</p></noscript>
<script id="ui" type="application/json">{ui_json}</script>
<script>{js}</script>
</body>
</html>
'''


def build(out):
    for lang, ui in UI.items():
        root = os.path.join(HERE, lang, 'project')
        deck = json.load(open(os.path.join(root, 'deck.json'), encoding='utf-8'))
        sections = ''.join(
            BLOB.sub(placeholder, isolate_embeds(open(os.path.join(root, 'slides', f'{sid}.html'), encoding='utf-8').read()))
            for sid in deck['order'])
        data = json.dumps(dict(other=ui['other'], slide=ui['slide'], of=ui['of']), ensure_ascii=False)
        page = PAGE.format(
            lang=lang, title=deck['title'], site=SITE, other_dir=UI[ui['other_lang']]['dir'], fonts=FONTS,
            css=CSS, js=JS, sections=sections, repo_url=REPO, ui_json=data.replace('</', '<\\/'),
            **{f'icon_{name}': svg for name, svg in ICONS.items()}, **ui)
        os.makedirs(os.path.join(out, ui['dir']), exist_ok=True)
        open(os.path.join(out, ui['dir'], 'index.html'), 'w', encoding='utf-8').write(page)
        print('wrote', os.path.join(out, ui['dir'], 'index.html'), len(deck['order']), 'slides')
    icons = os.path.join(ROOT, 'assets', 'icons', 'v2', 'app-icon')
    shutil.copy(os.path.join(icons, 'app-icon.svg'), os.path.join(out, 'favicon.svg'))
    shutil.copy(os.path.join(icons, 'app-icon.png'), os.path.join(out, 'icon.png'))
    for lang in UI:
        shutil.copy(os.path.join(ROOT, 'docs', 'images', 'slides', f'cover-{lang}.jpg'), os.path.join(out, f'cover-{lang}.jpg'))


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_site'))

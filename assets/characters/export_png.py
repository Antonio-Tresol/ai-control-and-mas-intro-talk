"""Export every SVG in svg/on-dark and svg/on-light to a 512 x 512 transparent PNG in png/.
Uses headless Google Chrome (macOS path below)."""
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'v2':
    HERE = os.path.join(HERE, 'v2')  # python3 export_png.py v2
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SIZE = 512

for sub in ('on-dark', 'on-light'):
    src, dst = os.path.join(HERE, 'svg', sub), os.path.join(HERE, 'png', sub)
    os.makedirs(dst, exist_ok=True)
    for name in sorted(os.listdir(src)):
        if not name.endswith('.svg'):
            continue
        svg = open(os.path.join(src, name)).read().replace('<svg ', f'<svg width="{SIZE}" height="{SIZE}" ', 1)
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
            f.write(f'<!doctype html><html><body style="margin:0;background:transparent">{svg}</body></html>')
            page = f.name
        out = os.path.join(dst, name[:-4] + '.png')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--window-size={SIZE},{SIZE}',
                        '--default-background-color=00000000', f'--screenshot={out}', 'file://' + page],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        os.unlink(page)
    print(sub, len(os.listdir(dst)), 'png')

"""Screenshots with headless Chrome, Chromium or Edge, on macOS, Linux or Windows.

Set CHROME to a browser binary to skip the search, for example CHROME=/usr/bin/chromium.
"""
import functools
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

NAMES = ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome', 'msedge')
PATHS = (
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    r'%ProgramFiles%\Google\Chrome\Application\chrome.exe',
    r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe',
    r'%LocalAppData%\Google\Chrome\Application\chrome.exe',
    r'%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe',
    r'%ProgramFiles%\Microsoft\Edge\Application\msedge.exe',
)


@functools.lru_cache(maxsize=None)
def find_chrome():
    if os.environ.get('CHROME'):
        return os.environ['CHROME']
    for name in NAMES:
        found = shutil.which(name)
        if found:
            return found
    for path in map(os.path.expandvars, PATHS):
        if os.path.isfile(path):
            return path
    sys.exit('No Chrome, Chromium or Edge found. Install one, or set CHROME to its path.')


def file_url(path):
    return pathlib.Path(path).resolve().as_uri()


def screenshot(url, png_path, width, height, transparent=False, wait_ms=0):
    """Save a width x height screenshot of url (http, https or file) to png_path."""
    args = [find_chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars',
            f'--window-size={width},{height}', f'--screenshot={os.path.abspath(png_path)}']
    if transparent:
        args.append('--default-background-color=00000000')
    if wait_ms:
        args.append(f'--virtual-time-budget={wait_ms}')
    subprocess.run(args + [url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def svg_to_png(svg, png_path, width, height):
    """Render an SVG string, already sized width x height, to a transparent PNG."""
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(f'<!doctype html><html><body style="margin:0;background:transparent">{svg}</body></html>')
    try:
        screenshot(file_url(f.name), png_path, width, height, transparent=True)
    finally:
        os.unlink(f.name)

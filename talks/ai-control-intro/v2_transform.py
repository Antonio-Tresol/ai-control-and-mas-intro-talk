# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Apply the v2 look to published slide files in place: black eyes with white centres, red attack colour.

Usage: uv run v2_transform.py <folder with project/slides/*.html> ...
Edits only the agent eyes, the attack colour and the words that describe that colour.
"""
import os
import re
import sys

RED = '#FF3B5C'
TEXT = [('reddish-purple', 'red'), ('reddish purple', 'red'), ('pink iris', 'red eye'),
        ('una bandera rojo púrpura', 'una bandera roja'), ('rombos rojo púrpura', 'rombos rojos'), ('rojo púrpura', 'rojo')]


def transform(s):
    n_iris = len(re.findall(r'r="12" fill="#0B1026"', s, re.I))
    s = re.sub(r'r="12" fill="#0B1026"', 'r="12" fill="@@WHITE@@"', s, flags=re.I)
    n_sclera = len(re.findall(r'<circle cx="50" cy="48" r="24" fill="#FDFBFF"/>', s, re.I))
    s = re.sub(r'<circle cx="50" cy="48" r="24" fill="#FDFBFF"/>', '<circle cx="50" cy="48" r="24" fill="#0B1026"/>', s, flags=re.I)
    s = s.replace('@@WHITE@@', '#FDFBFF')
    s, n_hl = re.subn(r'<circle cx="[\d.]+" cy="[\d.]+" r="4" fill="#FDFBFF" stroke="none"/>', '', s, flags=re.I)
    s, n_red = re.subn(r'#DA86B4', RED, s, flags=re.I)
    n_txt = 0
    for a, b in TEXT:
        n_txt += s.count(a)
        s = s.replace(a, b)
    return s, (n_sclera, n_iris, n_hl, n_red, n_txt)


for root in sys.argv[1:]:
    d = os.path.join(root, 'project', 'slides')
    changed = []
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        s = open(p, encoding='utf-8').read()
        t, counts = transform(s)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t)
            changed.append(name)
        print(f'{name:22s} eyes {counts[0]:3d} iris {counts[1]:3d} highlights {counts[2]:3d} red {counts[3]:3d} words {counts[4]}')
    print(root.split('/')[-1], 'changed:', ' '.join(changed))

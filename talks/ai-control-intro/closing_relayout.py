# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
import re, sys
LAYOUT = {  # credits, label, small QR, "About me", personal URL
    'en': dict(team='5 mentees, mostly AI software and security engineers', c=556, l=680, q=772),
    'es': dict(team='5 mentees, en su mayoría ingenieros de software en IA y de seguridad', c=556, l=718, q=800),
}
LABEL = 'sparai.org · In-the-Wild AI Control'
for path, lang in ((sys.argv[1], 'en'), (sys.argv[2], 'es')):
    L = LAYOUT[lang]
    s = open(path, encoding='utf-8').read()
    subs = [
        (r'(<p style="position:absolute; top:)552(px; left:128px; width:)1000(px;[^>]*><span[^>]*>[^<]*</span><br>)[^<]*(</p>)',
         lambda m: f'{m.group(1)}{L["c"]}{m.group(2)}1040{m.group(3)}{L["team"]}{m.group(4)}'),
        (r'(<p style="position:absolute; top:)716(px;[^>]*>)sparai\.org/projects/f26/rec8RybPH2kNV6qDa(</p>)',
         lambda m: f'{m.group(1)}{L["l"]}{m.group(2)}{LABEL}{m.group(3)}'),
        (r'top:776px; left:128px; width:140px', lambda m: f'top:{L["q"]}px; left:128px; width:140px'),
        (r'top:788px; left:290px', lambda m: f'top:{L["q"]+12}px; left:290px'),
        (r'top:840px; left:290px', lambda m: f'top:{L["q"]+64}px; left:290px'),
    ]
    for pat, rep in subs:
        s, n = re.subn(pat, rep, s)
        assert n == 1, (lang, pat, n)
    open(path, 'w', encoding='utf-8').write(s)
    print(lang, 'ok')

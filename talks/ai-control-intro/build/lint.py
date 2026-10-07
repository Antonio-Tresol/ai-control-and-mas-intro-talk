import re, sys
html=open(sys.argv[1] if len(sys.argv)>1 else '../specimen.html').read()
html=re.sub(r'<aside>.*?</aside>', '', html, flags=re.S)  # speaker notes are not slide content
secs=re.findall(r'(<section .*?</section>)', html, re.S)
print('slides', len(secs))
bad=0
for i,s in enumerate(secs,1):
    sid=re.search(r'id="([^"]+)"',s).group(1)
    probs=[]
    for pat,msg in [(r'\bclass=', 'class'), (r'margin', 'margin'), (r'var\(', 'var()'), (r'\d(em|rem)\b', 'em/rem'),
                    (r'z-index', 'z-index'), (r'<text', 'svg text'), (r'<style', 'style tag'), (r'vw|vh', 'vw/vh')]:
        if re.search(pat, s): probs.append(msg)
    sizes=[int(x) for x in re.findall(r'font-size:(\d+)px', s)]
    small=[x for x in sizes if x<40]
    # footer citations/slide number are the stated 28px exception
    n28=len([x for x in sizes if x==28]); 
    if any(x<28 for x in sizes): probs.append(f'font<28 {sorted(set(x for x in sizes if x<28))}')
    if n28>2: probs.append(f'{n28} elements at 28px (expected 2 footer items)')
    if [x for x in small if x!=28]: probs.append(f'font<40 {sorted(set(small))}')
    # element count (tags opened) excluding svg internals
    body=re.sub(r'<svg.*?</svg>', '<svg></svg>', s, flags=re.S)
    els=len(re.findall(r'<(?!/)(?!br)[a-z0-9-]+', body))
    if els>200: probs.append(f'{els} elements')
    svgs=re.findall(r'<svg.*?</svg>', s, re.S)
    big=[len(x.encode()) for x in svgs if len(x.encode())>52000]
    if big: probs.append(f'svg over 52KB {big}')
    for x in svgs:
        if 'aria-label' not in x[:400]: probs.append('svg without aria-label')
    hexes=set(re.findall(r'#[0-9A-Fa-f]{6}\b', body))
    print(f'{i:02d} {sid:20s} elements={els:3d} svgs={len(svgs)} maxsvg={max([len(x.encode()) for x in svgs] or [0])//1024}KB sizes={sorted(set(sizes))} {"; ".join(probs) or "ok"}')
    bad+=bool(probs)
print('problems' if bad else 'all slides pass')

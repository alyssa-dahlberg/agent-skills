import re, pathlib, urllib.parse

import sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
files = {p: p.read_text() for p in root.rglob('*.md') if 'fixtures' not in str(p)}

def slugs(text):
    out = set()
    for line in text.splitlines():
        m = re.match(r'^#{1,6}\s+(.*)', line)
        if m:
            s = m.group(1).lower()
            s = re.sub(r'[^\w\s-]', '', s)
            out.add(re.sub(r'\s+', '-', s.strip()))
    return out

bad = 0
for p, t in files.items():
    for m in re.finditer(r'\]\(([^)]+)\)', t):
        target = m.group(1)
        if target.startswith('http'):
            continue
        path, _, frag = target.partition('#')
        dest = (p.parent / path).resolve() if path else p.resolve()
        if path and not dest.exists():
            print('MISSING FILE ', p.name, '->', target); bad += 1; continue
        if frag:
            key = [k for k in files if k.resolve() == dest]
            if not key:
                continue
            if urllib.parse.unquote(frag) not in slugs(files[key[0]]):
                print('DEAD ANCHOR  ', p.name, '->', target); bad += 1
print('problems:', bad)

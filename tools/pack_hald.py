"""Resample the RawTherapee HaldCLUT pack (level 12, 144^3) to 33^3 and pack each brand folder into one PNG.
Layout per group PNG: width 33*33, 33 rows per LUT; row = blue, column = red + 33*green (red fastest)."""
import sys, os, re, json
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
N = 33

def resample(path):
    im = Image.open(path)
    W = im.size[0]; L = round(W ** (1 / 3)); S = L * L
    assert im.size == (W, W) and L ** 3 == W, (path, im.size)
    t = np.arange(N) * (S - 1) / (N - 1)
    i0 = np.floor(t).astype(int); i1 = np.minimum(i0 + 1, S - 1); f = t - i0
    a = np.asarray(im.convert('RGB'), dtype=np.float32).reshape(S, S, S, 3)  # [b][g][r][ch]
    # separable trilinear: along r (axis 2), then g (axis 1), then b (axis 0)
    a = a[:, :, i0] * (1 - f)[None, None, :, None] + a[:, :, i1] * f[None, None, :, None]
    a = a[:, i0] * (1 - f)[None, :, None, None] + a[:, i1] * f[None, :, None, None]
    a = a[i0] * (1 - f)[:, None, None, None] + a[i1] * f[:, None, None, None]
    return np.clip(np.rint(a), 0, 255).astype(np.uint8)  # [b][g][r][ch]

def nice(name, brand):
    name = re.sub(r'\.png$', '', name)
    m = re.match(r'^(.*?)\s(\d)\s?([-+]*)$', name)       # "Portra 400 1 -" -> "Portra 400 −"
    if m: name = m.group(1) + (' ' + m.group(3).replace('-', '−') if m.group(3) else '')
    if name.lower().startswith(brand.lower() + ' '): name = name[len(brand) + 1:]
    return name.strip()

def key(n):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', n)]

index = []
for top, label in (('Color', 'Colour'), ('Black-and-White', 'Black and White')):
    for brand in sorted(os.listdir(os.path.join(src, top))):
        d = os.path.join(src, top, brand)
        if not os.path.isdir(d): continue
        files = sorted([x for x in os.listdir(d) if x.lower().endswith('.png') and not x.startswith('.')], key=key)
        cubes, names = [], []
        for fn in files:
            cubes.append(resample(os.path.join(d, fn)).reshape(N, N * N, 3))  # rows=b, cols=r+33g
            names.append(nice(fn, brand.split('-')[0]))
        slug = re.sub(r'[^a-z0-9]+', '-', f'{label}-{brand}'.lower()).strip('-')
        Image.fromarray(np.concatenate(cubes, axis=0)).save(os.path.join(out, slug + '.png'), optimize=True)
        index.append({'g': f'{label} / {brand.replace("-", " ")}', 's': slug, 'n': names})
        print(slug, len(names), os.path.getsize(os.path.join(out, slug + '.png')), flush=True)
json.dump(index, open(os.path.join(out, 'index.json'), 'w'), ensure_ascii=False, separators=(',', ':'))

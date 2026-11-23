"""Derive 400px-tall thumbnails for the home image wall from existing gallery images.

Run from the repository root:  python scripts/make_wall_thumbs.py   (requires Pillow)
Originals are untouched; thumbnails go to frontend/public/images/achievements/wall/.
"""
import tomllib
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[1] / 'frontend'
data = tomllib.loads((root / 'src/data/gallery.toml').read_text(encoding='utf-8'))
out = root / 'public/images/achievements/wall'
out.mkdir(parents=True, exist_ok=True)
seen = set()
total_in = total_out = 0
for key in ('waterfall_a', 'waterfall_b'):
    for item in data[key]:
        src = root / 'public' / item['src'].lstrip('/')
        if src.name in seen:
            continue
        seen.add(src.name)
        with Image.open(src) as im:
            im = im.convert('RGB')
            h = min(400, im.height)
            w = round(im.width * h / im.height)
            im.resize((w, h), Image.LANCZOS).save(out / src.name, 'WEBP', quality=80, method=6)
        total_in += src.stat().st_size
        total_out += (out / src.name).stat().st_size
print(f'{len(seen)} thumbnails, {total_in // 1024} KB -> {total_out // 1024} KB')

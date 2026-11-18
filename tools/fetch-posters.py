"""Download real Rutube poster images once; no API needed by visitors."""
import io
import json
import re
import urllib.request
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
content = root / 'assets/js/content.js'
text = content.read_text(encoding='utf-8')

def replace(match):
    video_id = match.group(2)
    request = urllib.request.Request(f'https://rutube.ru/api/video/{video_id}/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        info = json.load(response)
    with urllib.request.urlopen(info['thumbnail_url'], timeout=30) as response:
        image = Image.open(io.BytesIO(response.read())).convert('RGB')
        image.thumbnail((1280, 720))
        target = root / f'assets/img/rutube-{video_id}.jpg'
        image.save(target, quality=85, optimize=True)
    print(f'Poster saved: {video_id}')
    return f"poster: 'assets/img/rutube-{video_id}.jpg',\n      rutube: 'https://rutube.ru/video/{video_id}/'"

text = re.sub(r"poster: '([^']+)',\s+rutube: 'https://rutube.ru/video/([a-f0-9]+)/'", replace, text)
content.write_text(text, encoding='utf-8')

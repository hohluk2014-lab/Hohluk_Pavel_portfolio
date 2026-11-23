from pathlib import Path
import re
from PIL import Image

roots = [
    Path('projects/foto/концерты и фестивали'),
    Path('projects/foto/мероприятия'),
    Path('projects/foto/спорт'),
    Path('projects/foto/портреты и личные съёмки'),
]
files = sorted(path for root in roots for path in root.rglob('*.jpg'))
entries = []
for path in files:
    event = path.parent.name
    width, height = Image.open(path).size
    event_lower = event.lower()
    if path.is_relative_to(roots[2]):
        meta = 'Спорт'
    elif path.is_relative_to(roots[3]):
        meta = 'Портрет'
    elif 'концерт' in event_lower or 'электропартизаны' in event_lower or 'карбаш' in event_lower:
        meta = 'Концерт'
    elif 'фестиваль' in event_lower or path.is_relative_to(roots[0]):
        meta = 'Фестиваль'
    else:
        meta = 'Мероприятие'
    year_match = re.search(r'(20\d{2})', event)
    short_date = re.search(r'\d{2}\.\d{2}\.(\d{2})(?!\d)', event)
    year = int(year_match.group(1)) if year_match else (2000 + int(short_date.group(1)) if short_date else None)
    if year is None and path.is_relative_to(roots[0]):
        year = 2024  # Existing concert collection metadata.
    year_field = f', year: {year}' if year is not None else ''
    rel = path.as_posix()
    category = 'concerts' if path.is_relative_to(roots[0]) else ('sport' if path.is_relative_to(roots[2]) else ('portraits' if path.is_relative_to(roots[3]) else 'events'))
    entries.append(
        f"    {{ src: '{rel}', w: {width}, h: {height},\n"
        f"      title: '{event}', event: '{event}', meta: '{meta}'{year_field},\n"
        f"      tags: ['{category}'], alt: '{meta}: {event}' }}"
    )

block = '  photos: [\n' + ',\n'.join(entries) + '\n  ],'
content_path = Path('assets/js/content.js')
text = content_path.read_text(encoding='utf-8')
text = re.sub(r'  photos: \[.*?\n  \],\n\n  films:', block + '\n\n  films:', text, count=1, flags=re.S)
content_path.write_text(text, encoding='utf-8')
print(f'Added {len(entries)} gallery photos from {len(roots)} folders')

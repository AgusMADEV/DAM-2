import csv
from pathlib import Path
from typing import Iterable
from domain.models import Activity


def export_csv(activities: Iterable[Activity], dest: str):
    p = Path(dest)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'category', 'date', 'duration_min', 'notes'])
        for a in activities:
            writer.writerow([a.id, a.title, a.category, a.date, a.duration_min, a.notes])


def import_csv(src: str):
    p = Path(src)
    if not p.exists():
        raise FileNotFoundError(src)
    result = []
    with p.open('r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = Activity.from_dict({
                'id': row.get('id') or None,
                'title': row.get('title', ''),
                'category': row.get('category', 'general'),
                'date': row.get('date', ''),
                'duration_min': int(row.get('duration_min', 0)),
                'notes': row.get('notes', '')
            })
            result.append(a)
    return result

import json
from pathlib import Path
from typing import List
from domain.models import Activity
from .filesystem import ensure_data_dirs, partition_path


class JsonActivityRepo:
    def __init__(self, path: str = 'data/store.json'):
        self.path = Path(path)
        ensure_data_dirs(self.path.parent)
        if not self.path.exists():
            self._write([])

    def _read(self) -> List[dict]:
        try:
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _write(self, data: List[dict]):
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def all(self) -> List[Activity]:
        return [Activity.from_dict(d) for d in self._read()]

    def save(self, activity: Activity):
        items = self._read()
        # replace if exists
        for i, d in enumerate(items):
            if d.get('id') == activity.id:
                items[i] = activity.to_dict()
                self._write(items)
                return
        items.append(activity.to_dict())
        self._write(items)

    def delete(self, activity_id: str):
        items = [d for d in self._read() if d.get('id') != activity_id]
        self._write(items)

    def find(self, activity_id: str):
        for d in self._read():
            if d.get('id') == activity_id:
                return Activity.from_dict(d)
        return None

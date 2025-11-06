import json, csv
from pathlib import Path
from typing import List
from domain import Appointment

class JsonAppointmentRepo:
    def __init__(self, path: str = 'data/appointments.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list:
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, data: list):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # CRUD
    def all(self) -> List[Appointment]:
        return [Appointment.from_dict(d) for d in self._read()]

    def save_many(self, items: List[Appointment]):
        self._write([a.to_dict() for a in items])

    def upsert(self, a: Appointment):
        items = self.all()
        for i,x in enumerate(items):
            if x.id == a.id:
                items[i] = a
                break
        else:
            items.append(a)
        self.save_many(items)

    def delete(self, id_: str):
        items = [a for a in self.all() if a.id != id_]
        self.save_many(items)
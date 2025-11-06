from dataclasses import dataclass, asdict, field
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class Activity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ''
    category: str = 'general'
    date: str = ''  # ISO date YYYY-MM-DD
    duration_min: int = 0
    notes: str = ''

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> 'Activity':
        return Activity(
            id=d.get('id', ''),
            title=d.get('title', ''),
            category=d.get('category', 'general'),
            date=d.get('date', ''),
            duration_min=int(d.get('duration_min', 0)),
            notes=d.get('notes', '')
        )

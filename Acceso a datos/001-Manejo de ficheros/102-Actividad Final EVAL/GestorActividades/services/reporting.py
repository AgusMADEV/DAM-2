from typing import List, Dict
from domain.models import Activity


def count_by_category(activities: List[Activity]) -> Dict[str, int]:
    d = {}
    for a in activities:
        d[a.category] = d.get(a.category, 0) + 1
    return d

def count_by_month(activities: List[Activity]) -> Dict[str, int]:
    d = {}
    for a in activities:
        key = a.date[:7] if a.date else 'unknown'
        d[key] = d.get(key, 0) + 1
    return d

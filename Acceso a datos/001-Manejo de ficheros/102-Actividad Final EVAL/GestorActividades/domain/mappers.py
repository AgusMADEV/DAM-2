"""Lugar para funciones de mapeo entre estructuras (placeholder).
En este esqueleto dejamos funciones simples para futuro uso.
"""
from .models import Activity


def dict_to_activity(d: dict) -> Activity:
    return Activity.from_dict(d)


def activity_to_dict(a: Activity) -> dict:
    return a.to_dict()

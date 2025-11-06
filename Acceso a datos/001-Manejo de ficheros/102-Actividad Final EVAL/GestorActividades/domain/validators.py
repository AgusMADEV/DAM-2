from datetime import datetime


def parse_date(text: str):
    try:
        return datetime.strptime(text, '%Y-%m-%d').date()
    except Exception:
        return None


def valid_date(text: str) -> bool:
    return parse_date(text) is not None


def valid_duration(value) -> bool:
    try:
        return int(value) >= 0
    except Exception:
        return False

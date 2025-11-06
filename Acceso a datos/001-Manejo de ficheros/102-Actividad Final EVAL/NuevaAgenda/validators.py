import re
from datetime import datetime

FECHA_FMT = '%d/%m/%Y'
HORA_FMT = '%H:%M'

def v_fecha(s: str) -> bool:
    try:
        datetime.strptime(s, FECHA_FMT); return True
    except Exception:
        return False

def v_hora(s: str) -> bool:
    try:
        datetime.strptime(s, HORA_FMT); return True
    except Exception:
        return False

def v_telefono(s: str) -> bool:
    if not s: return True
    digits = re.sub(r'\D','', s)
    return len(digits) == 9
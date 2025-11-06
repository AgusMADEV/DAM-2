from pathlib import Path


def ensure_data_dirs(base: Path):
    base.mkdir(parents=True, exist_ok=True)
    (base / 'export').mkdir(parents=True, exist_ok=True)


def partition_path(base: Path, date_str: str) -> Path:
    """Devuelve una carpeta de partición YYYY/MM dentro de base según date_str (ISO YYYY-MM-DD)."""
    try:
        year = date_str[:4]
        month = date_str[5:7]
        p = base / year / month
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        return base

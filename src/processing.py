def divide(a, b):
    return a / b


import re
from datetime import datetime
from typing import Dict, List, Optional


def _parse_date_for_sort(value: Optional[str]) -> Optional[datetime]:
    """Try to parse several date formats, return datetime or None."""
    if not value:
        return None

    s = value.strip()
    m_iso = re.match(r"^(\d{4}-\d{2}-\d{2})", s)
    if m_iso:
        try:
            return datetime.strptime(m_iso.group(1), "%Y-%m-%d")
        except ValueError:
            return None

    m_dd = re.match(r"^(\d{2}\.\d{2}\.\d{4})", s)
    if m_dd:
        try:
            return datetime.strptime(m_dd.group(1), "%d.%m.%Y")
        except ValueError:
            return None

    return None


def filter_by_state(items: List[Dict], state: str) -> List[Dict]:
    """Return subset of items whose 'state' equals given state."""
    if not items:
        return []
    return [it for it in items if it.get("state") == state]


def sort_by_date(items: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Sort items by parsed 'date' key. Items with missing/unparsed dates
    are considered minimal (come last when descending).
    """
    def key_fn(it: Dict) -> datetime:
        dt = _parse_date_for_sort(it.get("date") if isinstance(it, dict) else None)
        return dt if dt is not None else datetime.min

    return sorted(items, key=key_fn, reverse=descending)

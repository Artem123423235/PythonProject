# src/widget.py
"""
Widget utilities.

Содержит:
- mask_account_card(text): маскирует номера карт и счетов в строке.
- get_date(iso_str): преобразует ISO-дату -> "ДД.ММ.ГГГГ".
"""

import re
from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def _all_digits(text: str) -> str:
    """Return concatenated digits from text."""
    if not text:
        return ""
    return "".join(re.findall(r"\d", text))


def mask_account_card(text: str) -> str:
    """
    Replace digits in text with masked digits according to card/account rules.

    Decision rule:
    - If total digits == 20 -> treat as account (mask all but last 4).
    - Else if total digits >= 13 -> treat as card (keep first 6 and last 4).
    - Otherwise -> treat as account.
    """
    if not text:
        return text

    digits = _all_digits(text)
    if not digits:
        return text

    # Changed decision: 20-digit strings are accounts (common for bank accounts)
    if len(digits) == 20:
        masked = get_mask_account(digits)
    elif len(digits) >= 13:
        masked = get_mask_card_number(digits)
    else:
        masked = get_mask_account(digits)

    result = []
    it = iter(masked)
    for ch in text:
        if ch.isdigit():
            try:
                result.append(next(it))
            except StopIteration:
                result.append("*")
        else:
            result.append(ch)

    remaining = "".join(it)
    if remaining:
        result.append(remaining)

    return "".join(result)


def get_date(date_str: str) -> str:
    """
    Normalize date to DD.MM.YYYY format.

    Accepts:
    - 'YYYY-MM-DD' or 'YYYY-MM-DD...' (ISO at start)
    - 'DD.MM.YYYY' (already correct)
    If input empty/None -> return empty string.
    Otherwise return stripped input if not recognized.
    """
    if not date_str:
        return ""

    s = date_str.strip()
    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", s):
        return s

    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d")
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            return s

    return s
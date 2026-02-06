import re
from datetime import datetime
from typing import Optional

from src.masks import get_mask_account, get_mask_card_number


def _all_digits(text: Optional[str]) -> str:

    if not text:
        return ""
    return "".join(re.findall(r"\d", text))


def get_date(date_str: Optional[str]) -> str:

    if not date_str:
        return ""

    s = str(date_str).strip()
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


def mask_account_card(text: str) -> str:

    if not text:
        return text

    digits = _all_digits(text)
    if not digits:
        return text

    if len(digits) == 20:
        masked = get_mask_account(digits)
    elif len(digits) >= 13:
        masked = get_mask_card_number(digits)
    else:
        masked = get_mask_account(digits)

    # Попытка найти один "блок" с разделителями между группами цифр,
    # например "1111-2222-3333-4444" или "1111 2222 3333 4444".
    sep_group_pattern = re.compile(r"\d+(?:[ \-]\d+)+")
    for m in sep_group_pattern.finditer(text):
        group = m.group(0)
        group_digits = "".join(re.findall(r"\d", group))
        if group_digits and group_digits == digits:
            return text[: m.start()] + masked + text[m.end() :]

    # Если нет подходящего блока, применяем замену по позициям, сохраняя остальные символы
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

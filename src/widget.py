# src/widget.py
"""
Widget utilities.

Содержит:
- mask_account_card(text): маскирует номера карт и счетов в строке.
- get_date(iso_str): преобразует ISO-дату -> "ДД.ММ.ГГГГ".
"""

from datetime import datetime
from typing import Callable, Optional
import re

_external_mask_card: Optional[Callable[[str], str]] = None
_external_mask_account: Optional[Callable[[str], str]] = None

# Попытка переиспользовать внешние реализации, если они есть.
# Импорт выполняем в try/except, чтобы не ломать модуль при отсутствии этих библиотек.
try:
    # ожидание имен функций: mask_card_number, mask_account_number
    from masking import mask_card_number as _external_mask_card  # type: ignore
except Exception:
    _external_mask_card = None

if _external_mask_card is None:
    try:
        from utils import mask_card_number as _external_mask_card  # type: ignore
    except Exception:
        _external_mask_card = None

try:
    from masking import mask_account_number as _external_mask_account  # type: ignore
except Exception:
    _external_mask_account = None

if _external_mask_account is None:
    try:
        from utils import mask_account_number as _external_mask_account  # type: ignore
    except Exception:
        _external_mask_account = None


def _mask_card_number_default(number: str) -> str:
    """
    Базовая маскировка для карт.

    Пример поведения для 16-значной карты:
    7000792289606361 -> 7000 79** **** 6361

    Для других длин: показываем первые 4 и последние 4, середину заменяем '*'
    и группируем по 4 символа для читаемости.
    """
    digits = re.sub(r"\D", "", number)
    if not digits:
        return number

    if len(digits) == 16:
        return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"

    if len(digits) <= 8:
        return digits[:4] + "*" * max(0, len(digits) - 4)

    first = digits[:4]
    last = digits[-4:]
    middle_len = len(digits) - 8
    middle = "*" * middle_len
    groups = [middle[i : i + 4] for i in range(0, len(middle), 4)]
    return " ".join([first] + groups + [last])


def _mask_account_number_default(number: str) -> str:
    """
    Базовая маскировка для счетов: показываем только последние 4 цифры.
    Пример: 73654108430135874305 -> **4305
    """
    digits = re.sub(r"\D", "", number)
    if not digits:
        return number
    return f"**{digits[-4:]}"


_mask_card_number: Callable[[str], str] = (
    _external_mask_card or _mask_card_number_default
)
_mask_account_number: Callable[[str], str] = (
    _external_mask_account or _mask_account_number_default
)


def mask_account_card(text: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Аргумент:
        text: строка вида "Visa Platinum 7000792289606361" или
              "Счет 73654108430135874305".

    Возвращает:
        Строку с замаскированным номером.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    parts = text.rsplit(" ", 1)
    if len(parts) == 1:
        return text

    name, number = parts
    if name.strip().lower().startswith("счет"):
        masked = _mask_account_number(number)
    else:
        masked = _mask_card_number(number)

    return f"{name} {masked}"


def get_date(iso_str: str) -> str:
    """
    Преобразует строку-дату из ISO-формата
    ("2024-03-11T02:26:18.671407") в формат "ДД.MM.ГГГГ".

    Бросает ValueError при неверном формате.
    """
    if not isinstance(iso_str, str):
        raise TypeError("iso_str must be a string")

    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%d.%m.%Y")


__all__ = ["mask_account_card", "get_date"]
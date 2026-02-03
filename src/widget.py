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


def get_mask_account_card(account_number):
    """Функция для маскирования номера счета."""
    if not isinstance(account_number, str):
        return "Некорректные данные: должен быть строковый тип"

    # Удаляем пробелы и дефисы из строки
    account_number = account_number.replace(" ", "").replace("-", "")

    if len(account_number) < 4:
        return "Номер счета слишком короткий"

    # Маскируем все, кроме последних 4 символов
    return '*' * (len(account_number) - 4) + account_number[-4:]


def get_date(date_str):
    """Преобразует строку даты в объект datetime."""
    if not date_str:
        return "Строка даты отсутствует"

    # Попробуем разные форматы
    formats = [
        "%Y-%m-%d",  # 2023-10-25
        "%d-%m-%Y",  # 25-10-2023
        "%m/%d/%Y",  # 10/25/2023
        "%Y/%m/%d",  # 2023/10/25
        "%d %B %Y",  # 25 October 2023
        "%B %d, %Y"  # October 25, 2023
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return "Некорректный формат даты"
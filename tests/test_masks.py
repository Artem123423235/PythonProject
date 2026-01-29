# src/masks.py
"""
Модуль masks: маскировка номера карты и номера счёта.

Функции:
- get_mask_card_number(card_number: str | int) -> str
- get_mask_account(account_number: str | int) -> str
"""

import re
from typing import Union


def _only_digits_from_int_or_str(value: Union[int, str]) -> str:
    """Вернуть строку, содержащую только цифры из value."""
    s: str = str(value)
    return re.sub(r"\D", "", s)


def _group_by_4(s: str) -> str:
    """Разбить строку на группы по 4 символа, разделив пробелом."""
    return " ".join(s[i : i + 4] for i in range(0, len(s), 4))


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Маскирует номер банковской карты.

    Правило (как в тестах/критериях):
    - Показываем слева left_show = min(6, n - 4) цифр.
    - Показываем справа right_show = 4 цифры.
    - Средняя часть заменяется на '*' повторённую нужное число раз.
    - Для длины n <= 4 возвращается строка цифр без изменений.

    Аргумент может быть строкой с пробелами/дефисами или числом — используются только цифры.
    """
    digits: str = _only_digits_from_int_or_str(card_number)
    if not digits:
        raise ValueError("card_number must contain at least one digit")

    n: int = len(digits)
    if n <= 4:
        return digits

    left_show: int = min(6, max(0, n - 4))
    right_show: int = 4

    middle_len: int = n - left_show - right_show
    left: str = digits[:left_show]
    right: str = digits[-right_show:]

    middle_mask: str = "*" * middle_len if middle_len > 0 else ""
    masked: str = left + middle_mask + right

    return _group_by_4(masked)


def get_mask_account(account_number: Union[int, str]) -> str:
    """Маскирует номер счёта по правилу '**XXXX' (если длина > 4).

    Если длина цифр <= 4 — возвращает цифры как есть.
    """
    digits: str = _only_digits_from_int_or_str(account_number)
    if not digits:
        raise ValueError("account_number must contain at least one digit")

    if len(digits) <= 4:
        return digits

    return "**" + digits[-4:]

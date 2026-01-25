# src/masks.py
"""
Модуль masks: функции маскировки номера банковской карты и банковского счёта.
"""

import re


def _only_digits(value: str) -> str:
    """Вернуть только цифры из строки."""
    return "".join(re.findall(r"\d", value))


def _group_by_4(s: str) -> str:
    """Разбить строку на группы по 4 символа, разделитель — пробел."""
    return " ".join(s[i : i + 4] for i in range(0, len(s), 4))


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Правила:
    - Оставляются только цифры из входной строки.
    - Если длина <= 4: возвращается как есть (ничего не маскируется).
    - Иначе: показываются первые min(6, len-4) цифр и последние 4 цифры.
      Все промежуточные цифры заменяются на '*'.
    - Результат форматируется блоками по 4 символа, разделёнными пробелом.
    """
    digits = _only_digits(card_number)
    if not digits:
        raise ValueError("card_number must contain at least one digit")

    n = len(digits)
    if n <= 4:
        return digits

    left_show = min(6, n - 4)
    right_show = 4
    masked_mid_len = n - left_show - right_show
    masked = digits[:left_show] + ("*" * masked_mid_len) + digits[-right_show:]
    return _group_by_4(masked)


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта по правилу "**XXXX".

    Правила:
    - Оставляются только цифры из входной строки.
    - Если длина <= 4: возвращается как есть.
    - Иначе: возвращается строка, состоящая из двух звёздочек ('**')
      и последних 4 цифр номера, например "**4312".
    """
    digits = _only_digits(account_number)
    if not digits:
        raise ValueError("account_number must contain at least one digit")

    n = len(digits)
    if n <= 4:
        return digits

    return "**" + digits[-4:]
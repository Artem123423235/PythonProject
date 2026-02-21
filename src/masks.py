# src/masks.py

import re

def _only_digits(s: str) -> str:
    """Возвращает строку, содержащую только цифры из входной строки."""
    if s is None:
        return ""
    return "".join(re.findall(r"\d", s))


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в соответствии с тестами.

    Правила:
    - Убираем все не-цифровые символы.
    - Если после этого нет цифр -> ValueError.
    - Если цифр <= 4 -> возвращаем как есть (только цифры).
    - Если 5..15 цифр -> ValueError.
    - Если >= 16 цифр -> возвращаем в формате:
        "XXXX YYYY ** **** ZZZZ"
      где XXXX = первые 4, YYYY = следующие 4, ZZZZ = последние 4 цифры.
    """
    digits = _only_digits(card_number)

    if not digits:
        raise ValueError("card_number must contain at least one digit.")

    if len(digits) <= 4:
        return digits

    if len(digits) < 16:
        raise ValueError("card_number must contain at least 16 digits.")

    first4 = digits[:4]
    second4 = digits[4:8]
    last4 = digits[-4:]
    return f"{first4} {second4} ** **** {last4}"


def get_mask_account(account: str) -> str:
    """
    Маскирует номер счета в соответствии с тестами.

    Правила:
    - Убираем все не-цифровые символы.
    - Если после этого нет цифр -> ValueError.
    - Если цифр <= 4 -> возвращаем как есть (только цифры).
    - Если цифр > 4 -> маскируем часть слева звёздочками и возвращаем
      строку вида: '*' * mask_count + last4_digits
      где mask_count = min(total_digits - 4, 10)
      (т.е. не более 10 звёздочек; оставляем 4 последних цифры).
    """
    digits = _only_digits(account)

    if not digits:
        raise ValueError("account must contain at least one digit.")

    total_digits = len(digits)
    if total_digits <= 4:
        return digits

    mask_count = min(total_digits - 4, 10)
    return "*" * mask_count + digits[-4:]

# src/masks.py
"""
Модуль masks: функции маскировки номера банковской карты и банковского счёта.
"""


def get_mask_account(account_number):
    """Маскирует номер счета."""
    if not isinstance(account_number, str):
        return "Некорректные данные: должен быть строковый тип"

    account_number = account_number.replace(" ", "").replace("-", "")

    if len(account_number) < 4:
        return "Номер счета слишком короткий"

    return '*' * (len(account_number) - 4) + account_number[-4:]


def mask_account_card(card_number):
    """Маскирует номер карточки."""
    if not isinstance(card_number, str):
        return "Некорректные данные"

    card_number = card_number.replace(" ", "").replace("-", "")

    if len(card_number) < 4:
        return "Некорректные данные"

    return '*' * (len(card_number) - 4) + card_number[-4:]



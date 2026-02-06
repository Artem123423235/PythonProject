# src/masks.py
import re


def _digits(text: str) -> str:
    """Return only digit characters from text."""
    if not text:
        return ""
    return "".join(re.findall(r"\d", text))


def get_mask_card_number(card_str: str) -> str:
    """
    Mask card number: keep first 6 and last 4 digits if length >= 10.
    If length < 10 and > 4: mask all but last 4.
    If length <= 4 or no digits: return digits or empty string.
    """
    digits = _digits(card_str)
    n = len(digits)
    if n == 0:
        return ""
    if n <= 4:
        return digits
    if n < 10:
        return "*" * (n - 4) + digits[-4:]
    return digits[:6] + "*" * (n - 10) + digits[-4:]


def get_mask_account(account_str: str) -> str:
    """
    Mask account number: keep last 4 digits, mask the rest.
    If length <= 4: return digits unchanged.
    """
    digits = _digits(account_str)
    n = len(digits)
    if n == 0:
        return ""
    if n <= 4:
        return digits
    return "*" * (n - 4) + digits[-4:]

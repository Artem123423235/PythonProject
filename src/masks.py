import re
from decorators.log import setup_logger

logger = setup_logger('masks')


def example_function():
    try:
        logger.info("Функция example_function запущена.")

        # Логика функции...

        logger.info("Функция example_function успешно завершена.")
    except Exception as e:
        logger.error(f"Ошибка в функции example_function: {e}")


def _only_digits(s: str) -> str:
    if s is None:
        return ""
    return "".join(re.findall(r"\d", s))


def get_mask_card_number(card_number: str) -> str:
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
    digits = _only_digits(account)
    if not digits:
        raise ValueError("account must contain at least one digit.")
    total_digits = len(digits)
    if total_digits <= 4:
        return digits
    mask_count = min(total_digits - 4, 10)
    return "*" * mask_count + digits[-4:]

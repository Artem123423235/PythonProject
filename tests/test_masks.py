from src.masks import (get_mask_card_number, get_mask_account)

def test_get_mask_card_number():
    assert get_mask_card_number("1234567897415689") == "1234 56** **** 5689"

def get_mask_account(account_number):
    if len(account_number) < 4:
        return "Номер счета слишком короткий"

    # Маскируем все, кроме последних 4 цифр
    return '*' * (len(account_number) - 4) + account_number[-4:]


    def test_masking_correct_length(self):
        self.assertEqual(get_mask_account("1234567890"), "******7890")
        self.assertEqual(get_mask_account("987654321"), "*****4321")
        self.assertEqual(get_mask_account("1234"), "1234")

    def test_masking_various_formats(self):
        self.assertEqual(get_mask_account("12-34-56-78"), "****-**-78")
        self.assertEqual(get_mask_account("ABCD1234"), "****1234")

    def test_masking_shorter_than_expected(self):
        self.assertEqual(get_mask_account("123"), "Номер счета слишком короткий")
        self.assertEqual(get_mask_account("1"), "Номер счета слишком короткий")
        self.assertEqual(get_mask_account(""), "Номер счета слишком короткий")


def mask_account_card(account_card_number):
    """Функция маскирования номера карты или счета."""

    # Проверка на корректный ввод
    if not isinstance(account_card_number, str):
        return "Некорректные данные: должен быть строковый тип"

    # Удаляем пробелы и дефисы
    account_card_number = account_card_number.replace(" ", "").replace("-", "")

    if len(account_card_number) == 16:  # Логика для карт (например, Visa, MasterCard)
        return '*' * 12 + account_card_number[-4:]
    elif len(account_card_number) >= 4:  # Логика для счетов
        return '*' * (len(account_card_number) - 4) + account_card_number[-4:]
    else:
        return "Некорректные данные: слишком короткий номер"




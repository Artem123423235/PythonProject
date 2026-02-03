from src.widget import get_mask_account_card, get_date

def test_get_mask_account_card_number():

    def test_mask_card_number(self):
        self.assertEqual(mask_account_card("1234 5678 9012 3456"), "************3456")
        self.assertEqual(mask_account_card("1234-5678-9012-3456"), "************3456")
        self.assertEqual(mask_account_card("1234567890123456"), "************3456")

    def test_mask_account_number(self):
        self.assertEqual(mask_account_card("1234567890"), "******7890")
        self.assertEqual(mask_account_card("987654321"), "*****4321")
        self.assertEqual(mask_account_card("1234"), "1234")

    def test_incorrect_data_type(self):
        self.assertEqual(mask_account_card(1234567890123456), "Некорректные данные: должен быть строковый тип")
        self.assertEqual(mask_account_card(None), "Некорректные данные: должен быть строковый тип")

    def test_short_input(self):
        self.assertEqual(mask_account_card("123"), "Некорректные данные: слишком короткий номер")
        self.assertEqual(mask_account_card(""), "Некорректные данные: слишком короткий номер")


def test_get_test_get_date():

    def test_valid_date_formats(self):
        self.assertEqual(get_date("2023-10-25"), datetime(2023, 10, 25))
        self.assertEqual(get_date("25-10-2023"), datetime(2023, 10, 25))
        self.assertEqual(get_date("10/25/2023"), datetime(2023, 10, 25))
        self.assertEqual(get_date("2023/10/25"), datetime(2023, 10, 25))
        self.assertEqual(get_date("25 October 2023"), datetime(2023, 10, 25))
        self.assertEqual(get_date("October 25, 2023"), datetime(2023, 10, 25))

    def test_edge_cases(self):
        self.assertEqual(get_date("2023-02-29"), datetime(2023, 2, 28))  # Не высокосный год
        self.assertEqual(get_date("2020-02-29"), datetime(2020, 2, 29))  # Высокосный год
        self.assertEqual(get_date("01-01-2000"), datetime(2000, 1, 1))  # Переход в 2000 год

    def test_invalid_date_format(self):
        self.assertEqual(get_date("2023-25-10"), "Некорректный формат даты")
        self.assertEqual(get_date("25-13-2023"), "Некорректный формат даты")
        self.assertEqual(get_date("2023/10/32"), "Некорректный формат даты")

    def test_empty_string(self):
        self.assertEqual(get_date(""), "Строка даты отсутствует")
        self.assertEqual(get_date(None), "Строка даты отсутствует")
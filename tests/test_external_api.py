import unittest
from unittest.mock import patch, Mock
from external_api import (get_currency_rate, convert_to_rub)  # Импортируем функции из external_api.py


class TestCurrencyConversion(unittest.TestCase):

    @patch('requests.get')
    def test_get_currency_rate_success(self, mock_get):
        # Пример ответа от API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": {
                "RUB": 75.0,
                "USD": 1.0,
                "EUR": 0.85
            }
        }
        mock_get.return_value = mock_response

        rate = get_currency_rate("USD")
        self.assertEqual(rate, 75.0)

    @patch('requests.get')
    def test_get_currency_rate_rub_not_found(self, mock_get):
        # Пример ответа, когда RUB не найден
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": {
                "USD": 1.0,
                "EUR": 0.85
            }
        }
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            get_currency_rate("USD")
        self.assertEqual(str(context.exception), "Курс для RUB не найден.")

    @patch('requests.get')
    def test_get_currency_rate_invalid_response(self, mock_get):
        # Пример некорректного ответа от API
        mock_response = Mock()
        mock_response.status_code = 404  # Неудачный статус
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            get_currency_rate("USD")
        self.assertEqual(str(context.exception), "Не удалось получить курс валюты.")

    @patch('requests.get')
    def test_convert_to_rub_valid(self, mock_get):
        # Тест на успешную конвертацию
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": {
                "RUB": 75.0,
                "USD": 1.0,
                "EUR": 0.85
            }
        }
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = convert_to_rub(transaction)
        self.assertEqual(result, 7500.0)

    @patch('requests.get')
    def test_convert_to_rub_invalid_currency(self, mock_get):
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "INVALID"
                }
            }
        }

        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)

        self.assertEqual(str(context.exception), "Неподдерживаемая валюта.")

    @patch('requests.get')
    def test_convert_to_rub_invalid_structure(self, mock_get):
        transaction = {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }

        with self.assertRaises(ValueError) as context:
            convert_to_rub(transaction)

        self.assertEqual(str(context.exception), "Некорректная структура транзакции.")


if __name__ == '__main__':
    unittest.main()

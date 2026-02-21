import unittest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub


class TestExternalAPI(unittest.TestCase):

    @patch('requests.get')
    def test_convert_to_rub_valid(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "rates": {
                "RUB": 75.0
            }
        }
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 7500.0)

    @patch('requests.get')
    def test_convert_to_rub_invalid_currency(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": "Invalid currency"
        }
        mock_get.return_value = mock_response

        transaction = {"amount": 100, "currency": "INVALID"}
        with self.assertRaises(ValueError):
            convert_to_rub(transaction)


if __name__ == '__main__':
    unittest.main()

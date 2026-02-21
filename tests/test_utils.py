import unittest
from unittest.mock import patch, mock_open
from src.utils import load_transactions
import sys
import os
import unittest
from unittest.mock import patch, mock_open

# Добавляем src к пути Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import load_transactions  # Импортируем модуль после добавления пути

class TestUtils(unittest.TestCase):
    # Ваши тесты здесь


    @patch("builtins.open", new_callable=mock_open, read_data='[{"amount": 100, "currency": "USD"}]')
    def test_load_transactions_valid(self, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["amount"], 100)

    @patch("builtins.open", new_callable=mock_open, read_data='')
    def test_load_transactions_empty_file(self, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_transactions_file_not_found(self, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='{"not": "a list"}')
    def test_load_transactions_invalid_json(self, mock_file):
        result = load_transactions("dummy_path.json")
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
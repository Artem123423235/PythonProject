import unittest
import pytest
from masks import get_mask_card_number, get_mask_account

class TestMasks(unittest.TestCase):

    def test_get_mask_account(self):
        result = get_mask_account("4081781009991000")
        self.assertEqual(result, "**********1000")

    def test_get_mask_account_short(self):
        self.assertEqual(get_mask_account("1234"), "1234")  # Возвращает как есть
        self.assertEqual(get_mask_account("99"), "99")      # Возвращает как есть

    def test_get_mask_account_invalid_raises(self):
        with self.assertRaises(ValueError):
            get_mask_account("no digits here")

    def test_get_mask_card_number_standard_16(self):
        result = get_mask_card_number("1234567812345678")
        self.assertEqual(result, "1234 5678 ** **** 5678")

    def test_get_mask_card_number_with_spaces(self):
        result = get_mask_card_number("1234 5678 9012 3456")
        self.assertEqual(result, "1234 5678 ** **** 3456")

    def test_get_mask_card_number_short(self):
        self.assertEqual(get_mask_card_number("1234"), "1234")  # Возвращает как есть
        self.assertEqual(get_mask_card_number("12"), "12")      # Возвращает как есть

    def test_get_mask_card_number_non_digit_chars(self):
        result = get_mask_card_number("  4111-1111-1111-1111  ")
        self.assertEqual(result, "4111 1111 ** **** 1111")

    def test_get_mask_card_number_empty_raises(self):
        with self.assertRaises(ValueError):
            get_mask_card_number("abc")

if __name__ == '__main__':
    unittest.main()

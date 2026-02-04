import pytest
from src.masks import mask_account_card, get_mask_account

@pytest.mark.parametrize("card, expected", [
    ("1234 5678 9012 3456", "************3456"),
    ("1234-5678-9012-3456", "************3456"),
    ("1234567890123456", "************3456"),
    ("1234", "1234"),
    ("1234567890", "******7890"),
    (None, "Некорректные данные"),
])
def test_mask_account_card(card, expected):
    assert mask_account_card(card) == expected


@pytest.mark.parametrize("account, expected", [
    ("1234567890", "******7890"),
    ("1234", "1234"),
    (None, "Некорректные данные: должен быть строковый тип"),
])
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected




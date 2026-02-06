import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "inp,expected",
    [
        ("1111222233334444", "111122******4444"),
        ("1111 2222 3333 4444", "111122******4444"),
        ("12345678", "****5678"),
        ("no digits", ""),
    ],
    ids=["card_standard", "card_with_spaces", "card_short", "card_no_digits"],
)
def test_get_mask_card_number(inp, expected):
    assert get_mask_card_number(inp) == expected


@pytest.mark.parametrize(
    "inp,expected",
    [
        ("40817810099910004312", "*" * 16 + "4312"),
        ("123", "123"),
        ("abcd1234", "1234"),
    ],
    ids=["account_long", "account_short", "account_mixed_chars"],
)
def test_get_mask_account(inp, expected):
    assert get_mask_account(inp) == expected


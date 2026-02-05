from src.masks import get_mask_account, get_mask_card_number


def test_card_standard():
    assert get_mask_card_number("1111222233334444") == "111122******4444"


def test_card_with_spaces():
    assert get_mask_card_number("1111 2222 3333 4444") == "111122******4444"


def test_card_short():
    assert get_mask_card_number("12345678") == "****5678"


def test_card_no_digits():
    assert get_mask_card_number("no digits") == ""


def test_account_long():
    masked = "*" * 16 + "4312"
    assert get_mask_account("40817810099910004312") == masked


def test_account_short():
    assert get_mask_account("123") == "123"



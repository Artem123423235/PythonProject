# tests/test_masks.py
import pytest
from masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_standard_16():
    src = "1234 5678 9012 3456"
    masked = get_mask_card_number(src)
    assert masked == "1234 56** **** 3456"


def test_get_mask_card_number_short():
    # 8 digits -> left_show = min(6, 8-4)=4, right_show=4, masked_mid_len=0
    assert get_mask_card_number("12345678") == "1234 5678"


def test_get_mask_card_number_very_short():
    assert get_mask_card_number("1234") == "1234"
    assert get_mask_card_number("12") == "12"


def test_get_mask_card_number_non_digit_chars():
    assert get_mask_card_number("  4111-1111-1111-1111  ") == "4111 11** **** 1111"


def test_get_mask_card_number_empty_raises():
    with pytest.raises(ValueError):
        get_mask_card_number("abc")


def test_get_mask_account_standard():
    acc = "40817810099910004312"
    assert get_mask_account(acc) == "**4312"


def test_get_mask_account_short():
    assert get_mask_account("1234") == "1234"
    assert get_mask_account("99") == "99"


def test_get_mask_account_invalid_raises():
    with pytest.raises(ValueError):
        get_mask_account("no digits here")
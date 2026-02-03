from src.masks import (get_mask_card_number)

def test_get_mask_card_number():
    assert get_mask_card_number("1234567897415689") == "1234 56** **** 5689"

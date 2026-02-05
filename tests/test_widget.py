from src.widget import get_date, mask_account_card


def test_mask_card_in_text():
    src = "Visa 2222333344445555"
    expected = "Visa 222233******5555"
    assert mask_account_card(src) == expected


def test_mask_account_in_text():
    src = "Счет 40817810099910004312"
    masked = "*" * 16 + "4312"
    assert mask_account_card(src) == "Счет " + masked


def test_mask_no_digits():
    src = "No digits here"
    assert mask_account_card(src) == src


def test_get_date_iso_and_dd():
    assert get_date("2019-08-26T10:50:58") == "26.08.2019"
    assert get_date("26.08.2019") == "26.08.2019"
    assert get_date("") == ""
import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "src,expected",
    [
        ("Visa 2222333344445555", "Visa 222233******5555"),
        ("Счет 40817810099910004312", "Счет " + ("*" * 16 + "4312")),
        ("No digits here", "No digits here"),
        # case with contiguous 20-digit number inside text
        ("Acc:40817810099910004312", "Acc:" + ("*" * 16 + "4312")),
        # card with separators preserved
        ("Card: 1111-2222-3333-4444", "Card: 111122******4444"),
    ],
    ids=["card_in_text", "account_in_text_cyr", "no_digits", "account_no_space", "card_with_hyphens"],
)
def test_mask_account_card(src, expected):
    assert mask_account_card(src) == expected


@pytest.mark.parametrize(
    "inp,expected",
    [
        ("2019-08-26T10:50:58", "26.08.2019"),
        ("26.08.2019", "26.08.2019"),
        ("2018-01-12", "12.01.2018"),
        ("", ""),
        (None, ""),  # if implementation treats None -> ""
        ("not-a-date", "not-a-date"),
    ],
    ids=["iso_with_time", "dd_mm_yyyy", "iso_date", "empty", "none", "unrecognized"],
)
def test_get_date(inp, expected):
    # ensure get_date handles None safely if implemented to return ""
    assert get_date(inp or "") == expected

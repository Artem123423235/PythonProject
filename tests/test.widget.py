import pytest
from copy import deepcopy

from src.processing import filter_by_state, sort_by_date  # noqa: F401  # импорт для побочного эффекта

import src.widget as widget
from src.widget import mask_account_card, get_date


def test_filter_by_state_defaults_and_missing_key():
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3},  # нет 'state'
        {"id": 4, "state": "EXECUTED"},
        {"id": 5, "state": None},
    ]
    orig = deepcopy(data)
    res = filter_by_state(data)  # по умолчанию 'EXECUTED'
    assert res == [{"id": 1, "state": "EXECUTED"}, {"id": 4, "state": "EXECUTED"}]
    # убедимся, что исходный список не изменился
    assert data == orig


def test_filter_by_state_custom_value_and_empty():
    data = [
        {"id": 1, "state": "CANCELLED"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "CANCELLED"},
    ]
    res = filter_by_state(data, state="CANCELLED")
    assert res == [{"id": 1, "state": "CANCELLED"}, {"id": 3, "state": "CANCELLED"}]

    assert filter_by_state([]) == []  # пустой список возвращается как есть


def test_mask_card_number_default_16_digits():
    inp = "Visa Classic 7000792289606361"
    out = mask_account_card(inp)
    assert out == "Visa Classic 7000 79** **** 6361"


def test_mask_card_number_short_length():
    inp = "Card 12345678"
    out = mask_account_card(inp)
    # первые 4 цифры, затем 4 звездочки
    assert out == "Card 1234****"


def test_mask_card_number_other_length_grouping():
    # 12 цифр -> первые 4, затем одна группа middle(4), затем последние 4
    inp = "TestCard 123456789012"
    out = mask_account_card(inp)
    assert out == "TestCard 1234 **** 9012"


def test_mask_account_number_default():
    inp = "Счет 73654108430135874305"
    out = mask_account_card(inp)
    # по умолчанию: ** + последние 4 цифры
    assert out == "Счет **4305"


def test_mask_account_card_no_space_returns_original():
    s = "NoNumberHere"
    assert mask_account_card(s) == s


def test_mask_account_card_wrong_type_raises():
    with pytest.raises(TypeError):
        mask_account_card(12345)  # не строка


def test_get_date_valid_iso():
    iso = "2024-03-11T02:26:18.671407"
    assert get_date(iso) == "11.03.2024"


def test_get_date_invalid_format_raises_value_error():
    with pytest.raises(ValueError):
        # fromisoformat должен поднять ValueError для некорректной строки
        get_date("not-an-iso-date")


def test_get_date_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        get_date(None)


def test_mask_account_card_uses_overridden_maskers(monkeypatch):
    # Подменим внутренние функции маскировки и проверим, что они используются
    monkeypatch.setattr(widget, "_mask_card_number", lambda n: "<CARD>" + n)
    monkeypatch.setattr(widget, "_mask_account_number", lambda n: "<ACC>" + n)

    card_in = "Visa 0000111122223333"
    acc_in = "Счет 12345678901234567890"

    assert mask_account_card(card_in) == "Visa <CARD>0000111122223333"
    assert mask_account_card(acc_in) == "Счет <ACC>12345678901234567890"

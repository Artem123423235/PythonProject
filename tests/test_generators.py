# tests/test_generators.py
import re

from generators import (
    filter_by_currency,
    transaction_descriptions,
    _format_card_number,
    card_number_generator,
)


def test_filter_by_currency_basic_and_robustness():
    txs = [
        {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
        {"operationAmount": {"currency": {"code": "EUR"}}, "id": 2},
        {"operationAmount": {"currency": {"code": "USD"}}, "id": 3},
        {},  # пропускается: нет operationAmount
        "not a dict",  # пропускается
        {"operationAmount": {"currency": {"code": None}}},  # пропускается
        {"operationAmount": {"currency": {}}},  # пропускается: нет code
    ]

    result = list(filter_by_currency(txs, "USD"))
    assert len(result) == 2
    assert {r.get("id") for r in result} == {1, 3}

    # currency_code передан как int -> приводится к str
    txs2 = [{"operationAmount": {"currency": {"code": "840"}}}]
    assert list(filter_by_currency(txs2, 840)) == txs2

    # пустые/None входы -> пустой итератор
    assert list(filter_by_currency([], "USD")) == []
    assert list(filter_by_currency(None, "USD")) == []


def test_transaction_descriptions_various_inputs():
    txs = [
        {"description": "payment"},
        {},  # нет description -> ""
        "not a dict",  # не dict -> ""
        {"description": None},  # None -> ""
        {"description": ""},  # пустая строка остаётся ""
    ]
    out = list(transaction_descriptions(txs))
    assert out == ["payment", "", "", "", ""]


def test__format_card_number_padding_and_groups():
    assert _format_card_number(1) == "0000 0000 0000 0001"
    assert _format_card_number(0) == "0000 0000 0000 0000"
    assert _format_card_number(1234567890123456) == "1234 5678 9012 3456"
    s = _format_card_number(42)
    # формат: 4 групп по 4 цифры, разделённых пробелами; всего 19 символов
    assert re.fullmatch(r"(?:\d{4} ){3}\d{4}", s)
    assert len(s) == 19
    # убедимся, что без пробелов ровно 16 цифр
    assert len(s.replace(" ", "")) == 16


def test_card_number_generator_basic_range_and_order():
    got = list(card_number_generator(1, 3))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]
    assert got == expected


def test_card_number_generator_start_less_than_one_and_floats():
    # start < 1 приводится к 1
    assert list(card_number_generator(0, 2)) == [
        _format_card_number(1),
        _format_card_number(2),
    ]
    # float приводится к int
    assert list(card_number_generator(1.0, 3.0)) == [
        _format_card_number(1),
        _format_card_number(2),
        _format_card_number(3),
    ]


def test_card_number_generator_invalid_inputs_and_empty_generation():
    # None входы -> пусто
    assert list(card_number_generator(None, 10)) == []
    assert list(card_number_generator(1, None)) == []

    # нечисловые строки -> пусто
    assert list(card_number_generator("abc", "xyz")) == []

    # start > end -> пусто
    assert list(card_number_generator(10, 5)) == []


def test_card_number_generator_clipping_to_max():
    MAX = 10**16 - 1
    start = MAX - 1
    end = MAX + 1000  # выход за границу
    out = list(card_number_generator(start, end))
    assert out == [_format_card_number(MAX - 1), _format_card_number(MAX)]
    # последний номер — действительно MAX в 16 цифрах
    assert out[-1].replace(" ", "") == f"{MAX:016d}"

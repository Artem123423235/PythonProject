import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.mark.parametrize(
    "currency,expected_count",
    [("USD", 3), ("RUB", 2), ("EUR", 0)],
)
def test_filter_by_currency_counts(sample_transactions, currency, expected_count):
    gen = filter_by_currency(sample_transactions, currency)
    items = list(gen)
    assert len(items) == expected_count
    for item in items:
        assert item["operationAmount"]["currency"]["code"] == currency


def test_filter_by_currency_empty_and_malformed():
    # empty list -> generator yields nothing
    gen_empty = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(gen_empty)

    # malformed entries should be skipped, not raise
    malformed = [{"no": "operationAmount"}, "string", None]
    gen = filter_by_currency(malformed, "USD")
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_basic(sample_transactions):
    gen = transaction_descriptions(sample_transactions)
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert [next(gen) for _ in range(len(expected))] == expected
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_empty_and_malformed():
    gen_empty = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(gen_empty)

    gen_malformed = transaction_descriptions([None, 123, {"description": None}])
    assert next(gen_malformed) == ""
    assert next(gen_malformed) == ""
    assert next(gen_malformed) == ""


def test_card_number_generator_basic_range():
    gen = card_number_generator(1, 5)
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert list(gen) == expected


def test_card_number_generator_single_and_bounds():
    max_val = 10**16 - 1
    single = list(card_number_generator(1, 1))
    assert single == ["0000 0000 0000 0001"]

    # test upper bound formatting (just one item)
    top = list(card_number_generator(max_val, max_val))
    assert top == [" ".join(f"{max_val:016d}"[i:i + 4] for i in range(0, 16, 4))]
    # ensure generator ends when start > end
    empty = card_number_generator(5, 1)
    with pytest.raises(StopIteration):
        next(empty)

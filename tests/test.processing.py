import pytest
from copy import deepcopy

from src.processing import filter_by_state, sort_by_date


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


def test_filter_by_state_bad_input_raises_type_error():
    # если передать None вместо списка, генератор списка выдаст TypeError при итерировании
    with pytest.raises(TypeError):
        filter_by_state(None)


def test_sort_by_date_descending_and_ascending_and_stability():
    data = [
        {"id": "a", "date": "2024-01-01"},
        {"id": "b", "date": "2024-03-05"},
        {"id": "c", "date": "2024-03-05"},  # тот же date, проверим стабильность
        {"id": "d", "date": "2022-12-31"},
    ]
    orig = deepcopy(data)

    # по умолчанию descending=True
    desc = sort_by_date(data)
    assert [item["id"] for item in desc] == ["b", "c", "a", "d"]
    # стабильность: при одинаковой дате порядок b, c сохранён
    assert desc[0]["id"] == "b" and desc[1]["id"] == "c"

    # ascending
    asc = sort_by_date(data, descending=False)
    assert [item["id"] for item in asc] == ["d", "a", "b", "c"]

    # исходный список не должен поменяться
    assert data == orig


def test_sort_by_date_missing_key_raises_key_error():
    data = [{"id": 1, "date": "2024-01-01"}, {"id": 2}]  # второй элемент без 'date'
    with pytest.raises(KeyError):
        sort_by_date(data)

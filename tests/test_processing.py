import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state,expected_ids",
    [
        ("EXECUTED", [1, 3, 5, 6]),
        ("CANCELLED", [2]),
        ("NO", []),
    ],
    ids=["executed", "cancelled", "not_found"],
)
def test_filter_by_state(sample_operations, state, expected_ids):
    res = filter_by_state(sample_operations, state)
    ids = sorted([it["id"] for it in res])
    assert ids == expected_ids


@pytest.mark.parametrize(
    "descending,first_expected_set,last_expected_set",
    [
        (True, {1, 3}, {5, 6, 7}),
        (False, {5, 6, 7}, {1, 2, 3, 4}),
    ],
    ids=["sort_desc", "sort_asc"],
)
def test_sort_by_date(sample_operations, descending, first_expected_set, last_expected_set):
    sorted_ops = sort_by_date(sample_operations, descending=descending)
    ids = [it["id"] for it in sorted_ops]
    # check sets for first/last blocks (order inside set not important)
    assert set(ids[: len(first_expected_set)]) == first_expected_set
    assert set(ids[-len(last_expected_set) :]) == last_expected_set

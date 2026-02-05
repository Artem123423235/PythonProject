from src.processing import filter_by_state, sort_by_date


def test_filter_existing(sample_operations):
    res = filter_by_state(sample_operations, "EXECUTED")
    ids = sorted([it["id"] for it in res])
    assert ids == [1, 3, 5, 6]


def test_filter_none(sample_operations):
    assert filter_by_state(sample_operations, "NO") == []


def test_sort_descending(sample_operations):
    sorted_ops = sort_by_date(sample_operations, descending=True)
    ids = [it["id"] for it in sorted_ops]
    assert set(ids[:2]) == {1, 3}
    assert set(ids[-3:]) == {5, 6, 7}


def test_sort_ascending(sample_operations):
    sorted_ops = sort_by_date(sample_operations, descending=False)
    ids = [it["id"] for it in sorted_ops]
    assert set(ids[:3]) == {5, 6, 7}


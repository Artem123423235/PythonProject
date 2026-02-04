import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    return [
        {'name': 'Item 1', 'date': '2023-10-25', 'state': 'active'},
        {'name': 'Item 2', 'date': '2023-10-20', 'state': 'inactive'},
        {'name': 'Item 3', 'date': '2023-10-25', 'state': 'active'},  # Еще один объект с той же датой
        {'name': 'Item 4', 'date': '2023-09-15', 'state': 'pending'},
        {'name': 'Item 5', 'date': '2023/10/20', 'state': 'inactive'}  # Разные форматы
    ]

def test_sort_ascending(sample_data):
    sorted_items = sort_by_date(sample_data, reverse=False)
    expected_names = ['Item 4', 'Item 5', 'Item 2', 'Item 1', 'Item 3']
    assert [item['name'] for item in sorted_items] == expected_names


def test_sort_descending(sample_data):
    sorted_items = sort_by_date(sample_data, reverse=True)
    expected_names = ['Item 1', 'Item 3', 'Item 5', 'Item 2', 'Item 4']
    assert [item['name'] for item in sorted_items] == expected_names


def test_filter_by_state(sample_data):
    active_items = filter_by_state(sample_data, 'active')
    assert len(active_items) == 2
    assert all(item['state'] == 'active' for item in active_items)


def test_sort_by_date(sample_data):
        # Ожидаемый порядок
        expected_order = ['Item 3', 'Item 4', 'Item 2', 'Item 1']

        sorted_items = sort_by_date(sample_data, reverse=False)
        sorted_names = [item['name'] for item in sorted_items]

        assert sorted_names == expected_order

def test_sort_by_date_reverse(sample_data):
        # Ожидаемый порядок при обратной сортировке
        expected_order = ['Item 1', 'Item 2', 'Item 4', 'Item 3']

        sorted_items = sort_by_date(sample_data, reverse=True)
        sorted_names = [item['name'] for item in sorted_items]

        assert sorted_names == expected_order


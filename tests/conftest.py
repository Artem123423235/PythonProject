"""Common fixtures for tests."""
import pytest


@pytest.fixture
def sample_operations():
    """Provide sample operations for processing tests."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "state": "CANCELLED", "date": "2018-01-12"},
        {"id": 3, "state": "EXECUTED", "date": "2019-08-26"},
        {"id": 4, "state": "PENDING", "date": "26.08.2017"},
        {"id": 5, "state": "EXECUTED", "date": "not-a-date"},
        {"id": 6, "state": "EXECUTED", "date": None},
        {"id": 7, "state": "PROCESSING"},
    ]

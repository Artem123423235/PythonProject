from src.utils import calculate_logarithm, divide


def test_divide_simple():
    assert divide(6, 3) == 2


def test_divide_by_one():
    assert divide(a=2, b=1) == 2


def test_logarithm():
    assert calculate_logarithm(8, 2) == 3.0
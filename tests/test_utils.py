import math
import pytest

from src.utils import calculate_logarithm, divide


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (6, 3, 2),
        (2, 1, 2),
        (-4, 2, -2),
    ],
    ids=["six_div_three", "two_div_one", "negative_division"],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize(
    "x,base,expected",
    [
        (8, 2, 3.0),
        (27, 3, 3.0),
        (1, 10, 0.0),
    ],
    ids=["log2_8", "log3_27", "log_base_10_1"],
)
def test_calculate_logarithm(x, base, expected):
    assert pytest.approx(calculate_logarithm(x, base), rel=1e-9) == expected

from src.processing import divide

from main import calculate_logarithm


def test_divide():
    assert divide(a=2, b=1) == 2



def test_calc_log():
    assert calculate_logarithm(x=8, base=2) == 3.0
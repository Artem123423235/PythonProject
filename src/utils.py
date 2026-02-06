import math


def divide(a: float, b: float) -> float:
    """Return a / b (let Python raise ZeroDivisionError if b == 0)."""
    return a / b


def calculate_logarithm(x: float, base: float) -> float:
    """Return logarithm of x with given base."""
    return math.log(x, base)

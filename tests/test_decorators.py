import pytest
from decorators import log

@log()
def add(x: int, y: int) -> int:
    return x + y

def test_add(capsys):
    result = add(1, 2)
    assert result == 3
    captured = capsys.readouterr()
    assert "add ok" in captured.out


@log()
def divide(x: int, y: int) -> float:
    return x / y

def test_divide(capsys):
    result = divide(4, 2)
    assert result == 2.0
    captured = capsys.readouterr()
    assert "divide ok" in captured.out


def test_divide_by_zero(capsys):
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    # Проверяем имя ошибки и аргументы в stderr
    assert "divide error: ZeroDivisionError" in captured.err
    assert "(1, 0)" in captured.err
    assert "{}" in captured.err  # пустые kwargs

import os
import pathlib
import pytest

from decorators import log


def test_console_logging_success(capsys: pytest.CaptureFixture[str]) -> None:
    @log
    def add(x: int, y: int) -> int:
        return x + y

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    # Ожидаем, что в консоли присутствует сообщение о старте и сообщение об успешном завершении,
    # причём успешное сообщение содержит "add ok"
    assert "add start" in captured.out
    assert "add ok" in captured.out
    # опционально: результат должен быть в сообщении ok
    assert "5" in captured.out


def test_console_logging_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def fail_fn(a: int, b: int) -> int:
        raise ValueError("bad input")

    with pytest.raises(ValueError):
        fail_fn(1, 2)

    captured = capsys.readouterr()
    assert "fail_fn start" in captured.out
    # Проверяем, что зафиксирована ошибка и входные параметры
    assert "fail_fn error:" in captured.out
    assert "(1, 2)" in captured.out
    assert "{}" in captured.out  # пустые kwargs


def test_file_logging_success(tmp_path: pathlib.Path) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def greet(name: str) -> str:
        return f"Hello, {name}"

    res = greet("Alice")
    assert res == "Hello, Alice"

    # Проверяем содержимое файла
    text = log_file.read_text(encoding="utf-8")
    assert "greet start" in text
    assert "greet ok" in text
    assert "Hello, Alice" in text


def test_file_logging_error(tmp_path: pathlib.Path) -> None:
    log_file = tmp_path / "errlog.txt"

    @log(filename=str(log_file))
    def explode(x: int) -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        explode(10, )

    text = log_file.read_text(encoding="utf-8")
    assert "explode start" in text
    assert "explode error:" in text
    assert "(10,)" in text  # args tuple repr
    assert "{}" in text  # kwargs repr


def test_decorator_with_and_without_parentheses(tmp_path: pathlib.Path) -> None:
    # @log without parentheses
    @log
    def f1() -> str:
        return "ok1"

    # @log() with parentheses but without filename
    @log()
    def f2() -> str:
        return "ok2"

    # @log with filename
    file_path = tmp_path / "both.txt"

    @log(filename=str(file_path))
    def f3() -> str:
        return "ok3"

    assert f1() == "ok1"
    assert f2() == "ok2"
    assert f3() == "ok3"

    # проверяем, что файл exists and has the f3 entries
    content = file_path.read_text(encoding="utf-8")
    assert "f3 start" in content
    assert "f3 ok" in content

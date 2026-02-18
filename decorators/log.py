from __future__ import annotations

import functools
from typing import Any, Callable, Optional, TypeVar
from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def _write_log(message: str, filename: Optional[str]) -> None:
    """
    Записывает сообщение либо в файл (если filename задан), либо в stdout (print).
    """
    if filename:
        # Открываем каждый раз в режиме добавления, чтобы не сохранять состояние открытого файла
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


def log(func: Optional[Callable[P, R]] = None, *, filename: Optional[str] = None) -> Callable[..., Callable[P, R]]:
    """
    Декоратор, логирующий начало и конец выполнения функции, результат или ошибку.
    Поддерживает использование как @log, так и @log(filename="...").

    Формат логов:
    - Старт: "<func_name> start"
    - Успех: "<func_name> ok: <result_repr>"
    - Ошибка: "<func_name> error: <error_repr>. Inputs: <args_repr>, <kwargs_repr>"

    После логирования ошибка повторно возбуждается, чтобы поведение функции не изменялось.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _write_log(f"{fn.__name__} start", filename)
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 - намеренно ловим все исключения для логирования
                _write_log(
                    f"{fn.__name__} error: {exc}. Inputs: {args!r}, {kwargs!r}",
                    filename,
                )
                # повторно возбуждаем исключение, чтобы поведение было предсказуемым
                raise
            else:
                _write_log(f"{fn.__name__} ok: {result!r}", filename)
                return result

        return wrapper

    # Поддержка использования как @log и как @log(...)
    if callable(func):
        # Использование: @log
        return decorator(func)  # type: ignore[return-value]
    # Использование: @log(...) — возвращаем сам декоратор
    return decorator  # type: ignore[return-value]

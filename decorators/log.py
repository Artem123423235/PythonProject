from __future__ import annotations

import functools
import sys
from typing import Callable, Optional, TypeVar
from typing import ParamSpec
import logging
import os


def setup_logger(module_name):
    """Настраивает логгер для указанного модуля."""

    # Создаем папку logs, если она не существует
    logs_path = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    # Настройка формата логирования
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename=os.path.join(logs_path, f'{module_name}.log'),  # Путь к файлу лога
        filemode='w',  # Перезапись файла при каждом запуске
        format=log_format,
        level=logging.DEBUG  # Уровень логирования
    )

    logger = logging.getLogger(module_name)
    return logger


P = ParamSpec("P")
R = TypeVar("R")


def _write_log_to_file(message: str, filename: str) -> None:
    with open(filename, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def _print_to_console(message: str, *, err: bool = False) -> None:
    if err:
        print(message, file=sys.stderr)
    else:
        print(message)


def log(func: Optional[Callable[P, R]] = None, *, filename: Optional[str] = None) -> Callable[..., Callable[P, R]]:
    """
    Декоратор логирует:
      - "<func_name> start" (stdout)
      - при успехе: "<func_name> ok: <repr(result)>" (stdout)
      - при ошибке: "<func_name> error: <ExceptionType>. Inputs: <args_repr>, <kwargs_repr>"
        — при filename==None печатает в stderr, иначе пишет в файл.

    Поддерживает @log, @log() и @log(filename="...").
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_msg = f"{fn.__name__} start"
            if filename:
                _write_log_to_file(start_msg, filename)
            else:
                _print_to_console(start_msg, err=False)

            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                exc_name = type(exc).__name__
                err_msg = f"{fn.__name__} error: {exc_name}. Inputs: {args!r}, {kwargs!r}"
                if filename:
                    _write_log_to_file(err_msg, filename)
                else:
                    _print_to_console(err_msg, err=True)
                raise
            else:
                ok_msg = f"{fn.__name__} ok: {result!r}"
                if filename:
                    _write_log_to_file(ok_msg, filename)
                else:
                    _print_to_console(ok_msg, err=False)
                return result

        return wrapper

    if callable(func):
        return decorator(func)  # type: ignore[return-value]
    return decorator  # type: ignore[return-value]

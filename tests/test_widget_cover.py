# tests/test_widget_cover.py
import sys
import importlib
import types

import pytest

# Импортируем как пакет src.widget — pytest должен видеть пакет src (см. tests/conftest.py при необходимости)
import src.widget as widget
from src.widget import mask_account_card, get_date


def test_mask_card_number_default_16_digits():
    inp = "Visa Classic 7000792289606361"
    out = mask_account_card(inp)
    assert out == "Visa Classic 7000 79** **** 6361"


def test_mask_card_number_short_length():
    inp = "Card 12345678"
    out = mask_account_card(inp)
    assert out == "Card 1234****"  # первые 4, затем 4 звездочки


def test_mask_card_number_other_length_grouping():
    inp = "TestCard 123456789012"
    out = mask_account_card(inp)
    assert out == "TestCard 1234 **** 9012"  # 12 цифр -> middle_len=4 -> одна группа


def test_mask_account_number_default():
    inp = "Счет 73654108430135874305"
    out = mask_account_card(inp)
    assert out == "Счет **4305"


def test_mask_account_card_no_space_returns_original():
    s = "NoNumberHere"
    assert mask_account_card(s) == s


def test_mask_account_card_wrong_type_raises():
    with pytest.raises(TypeError):
        mask_account_card(12345)  # не строка


def test_mask_card_with_spaces_and_dashes():
    inp = "Card 1111-2222-3333-4444"
    # digits -> 1111222233334444 -> 16 digits, 1111 22** **** 4444
    assert mask_account_card(inp) == "Card 1111 22** **** 4444"


def test_get_date_valid_iso():
    iso = "2024-03-11T02:26:18.671407"
    assert get_date(iso) == "11.03.2024"


def test_get_date_invalid_format_raises_value_error():
    with pytest.raises(ValueError):
        get_date("not-an-iso-date")


def test_get_date_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        get_date(None)


def _reload_widget_with_modules(modules: dict):
    """
    Помощник: временно вставить модули в sys.modules и перезагрузить src.widget.
    modules: mapping name -> module object
    Возвращает: перезагруженный модуль
    """
    saved = {}
    for name, mod in modules.items():
        saved[name] = sys.modules.get(name)
        sys.modules[name] = mod
    try:
        m = importlib.reload(importlib.import_module("src.widget"))
    finally:
        # восстанавливать original sys.modules не будем здесь — тест сам очистит при необходимости
        pass
    return m, saved


def _cleanup_modules(saved):
    # saved: mapping name -> original module or None
    for name, orig in saved.items():
        if orig is None:
            # модуль был добавлен — удаляем
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = orig


def test_use_external_masking_module_preferred():
    # Создаём простой модуль masking с нужными функциями
    fake_masking = types.ModuleType("masking")
    fake_masking.mask_card_number = lambda s: "<EXT_CARD>" + s
    fake_masking.mask_account_number = lambda s: "<EXT_ACC>" + s

    # Сохраняем текущее состояние возможных модулей
    saved = {"masking": sys.modules.get("masking"), "utils": sys.modules.get("utils")}
    sys.modules["masking"] = fake_masking
    # Удаляем utils если есть, чтобы проверить приоритет masking над utils
    if "utils" in sys.modules:
        del sys.modules["utils"]

    try:
        # Перезагрузим модуль widget, чтобы он принял внешние реализации
        w = importlib.reload(importlib.import_module("src.widget"))
        assert w._mask_card_number is not None
        assert w._mask_account_number is not None

        assert w.mask_account_card("Visa 0000111122223333") == "Visa <EXT_CARD>0000111122223333"
        assert w.mask_account_card("Счет 12345678") == "Счет <EXT_ACC>12345678"
    finally:
        # Восстановим sys.modules и перезагрузим исходный модуль
        _cleanup_modules(saved)
        importlib.reload(importlib.import_module("src.widget"))


def test_utils_as_fallback_when_masking_missing():
    # Создаём модуль utils (и убедимся, что masking отсутствует)
    fake_utils = types.ModuleType("utils")
    fake_utils.mask_card_number = lambda s: "[UTIL_CARD]" + s
    fake_utils.mask_account_number = lambda s: "[UTIL_ACC]" + s

    saved = {"masking": sys.modules.get("masking"), "utils": sys.modules.get("utils")}
    # Удаляем masking если есть
    if "masking" in sys.modules:
        del sys.modules["masking"]
    sys.modules["utils"] = fake_utils

    try:
        w = importlib.reload(importlib.import_module("src.widget"))
        # Проверяем, что взяли реализации из utils
        assert w.mask_account_card("Visa 9999000011112222") == "Visa [UTIL_CARD]9999000011112222"
        assert w.mask_account_card("Счет 9876543210") == "Счет [UTIL_ACC]9876543210"
    finally:
        _cleanup_modules(saved)
        importlib.reload(importlib.import_module("src.widget"))
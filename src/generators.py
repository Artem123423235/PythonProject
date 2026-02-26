from typing import Iterable, Iterator, Optional

MAX_CARD = 10**16 - 1


def filter_by_currency(txs: Optional[Iterable], currency_code) -> Iterator[dict]:
    """
    Итератор по транзакциям, у которых operationAmount.currency.code == currency_code.
    Пропускает не-dict элементы, записи без operationAmount/currency/code или с code is None.
    currency_code приводится к str и сравнивается в верхнем регистре.
    """
    if not txs:
        return
        yield  # чтобы функция была генератором (ничего не отдаёт)

    target = str(currency_code).upper()

    for t in txs:
        if not isinstance(t, dict):
            continue
        op = t.get("operationAmount")
        if not isinstance(op, dict):
            continue
        cur = op.get("currency")
        if not isinstance(cur, dict):
            continue
        code = cur.get("code")
        if code is None:
            continue
        # нормализуем код (например, 840 -> "840")
        try:
            code_str = str(code).upper()
        except Exception:
            continue
        if code_str == target:
            yield t


def transaction_descriptions(txs: Optional[Iterable]) -> Iterator[str]:
    """
    Итератор строк описаний транзакций.
    Для некорректных записей/отсутствия description/None возвращает пустую строку "".
    """
    if not txs:
        return
        yield

    for t in txs:
        if not isinstance(t, dict):
            yield ""
            continue
        desc = t.get("description", "")
        if isinstance(desc, str):
            yield desc
        else:
            yield ""


def _format_card_number(n) -> str:
    """
    Форматирует число в 16-значный номер карты, группируя по 4 цифры через пробел.
    Пример: 1 -> "0000 0000 0000 0001"
             1234567890123456 -> "1234 5678 9012 3456"
    """
    try:
        i = int(n)
    except Exception:
        raise TypeError("_format_card_number expects an integer-convertible input")
    if i < 0:
        raise ValueError("Card number must be non-negative")
    # Формируем 16-значную строку с ведущими нулями
    s = f"{i:016d}"
    groups = [s[i:i+4] for i in range(0, 16, 4)]
    return " ".join(groups)


def card_number_generator(start, end) -> Iterator[str]:
    """
    Генератор форматированных номеров карт от start до end включительно.
    Правила:
    - Если start or end is None -> пусто.
    - Нецелые/float приводятся через int(); нечисловые строки -> пусто.
    - start < 1 приводится к 1.
    - Если start > end -> пусто.
    - Обрезает end по MAX_CARD (10**16 - 1).
    """
    if start is None or end is None:
        return
        yield

    try:
        s = int(start)
        e = int(end)
    except Exception:
        # нечисловые строки и т.п. -> ничего не генерируем
        return
        yield

    if s < 1:
        s = 1

    if s > e:
        return
        yield

    if s > MAX_CARD:
        return
        yield

    if e > MAX_CARD:
        e = MAX_CARD

    for i in range(s, e + 1):
        yield _format_card_number(i)

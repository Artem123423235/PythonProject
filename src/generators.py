from typing import Generator, Iterable, Iterator, List, Optional


def filter_by_currency(
    transactions: Optional[Iterable[dict]], currency_code: str
) -> Iterator[dict]:
    """
    Генератор: поочередно возвращает транзакции, у которых
    operationAmount.currency.code == currency_code.

    Устойчив к отсутствующим полям: пропускает некорректные записи.
    """
    if not transactions:
        return
        yield  # pragma: no cover

    code = str(currency_code)
    for tx in transactions:
        if not isinstance(tx, dict):
            continue
        op_amount = tx.get("operationAmount")
        if not isinstance(op_amount, dict):
            continue
        currency = op_amount.get("currency")
        if not isinstance(currency, dict):
            continue
        tx_code = currency.get("code")
        if tx_code == code:
            yield tx


def transaction_descriptions(transactions: Optional[Iterable[dict]]) -> Iterator[str]:
    """
    Генератор: поочередно возвращает поле 'description' для каждой транзакции.
    Если описание отсутствует — возвращает пустую строку.
    """
    if not transactions:
        return
        yield  # pragma: no cover

    for tx in transactions:
        if not isinstance(tx, dict):
            yield ""
            continue
        desc = tx.get("description")
        yield desc if desc is not None else ""


def _format_card_number(n: int) -> str:
    """Форматирует целое число в 'XXXX XXXX XXXX XXXX' с ведущими нулями."""
    s = f"{n:016d}"
    return " ".join(s[i : i + 4] for i in range(0, 16, 4))


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров карт (включительно): от start до end.
    Формат: '0000 0000 0000 0001' ... '9999 9999 9999 9999'.

    Поведение:
    - Если start > end — генерация завершится без выдачи значений.
    - Значения меньше 1 будут приведены к 1; значения больше максимума (10**16-1)
      ограничены максимумом.
    """
    if start is None or end is None:
        return
        yield  # pragma: no cover

    try:
        s = int(start)
        e = int(end)
    except (TypeError, ValueError):
        return
        yield  # pragma: no cover

    MAX_CARD = 10**16 - 1
    if s < 1:
        s = 1
    if e > MAX_CARD:
        e = MAX_CARD
    if s > e:
        return

    for n in range(s, e + 1):
        yield _format_card_number(n)

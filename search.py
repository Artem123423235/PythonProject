import re

def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Функция для фильтрации банковских операций по строке поиска в описании.

    :param data: Список словарей с транзакциями.
    :param search: Строка для поиска в описании транзакций.
    :return: Список словарей с подходящими транзакциями.
    """
    search_pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [transaction for transaction in data if search_pattern.search(transaction.get('description', ''))]

def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция для подсчета количества операций по категориям.

    :param data: Список словарей с транзакциями.
    :param categories: Список категорий для подсчета операций.
    :return: Словарь с количеством операций по категориям.
    """
    counts = {category: 0 for category in categories}
    for transaction in data:
        description = transaction.get('description', '')
        for category in categories:
            if category.lower() in description.lower():
                counts[category] += 1
    return counts

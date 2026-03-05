from collections import Counter


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция для подсчета количества операций по категориям.

    :param data: Список словарей с транзакциями.
    :param categories: Список категорий для подсчета операций.
    :return: Словарь с количеством операций по категориям.
    """
    counts = Counter()

    for transaction in data:
        description = transaction.get('description', '')
        for category in categories:
            if category.lower() in description.lower():
                counts[category] += 1

    return dict(counts)  # Конвертируем обратно в словарь

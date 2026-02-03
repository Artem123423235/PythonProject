def divide(a, b):
    return a / b


def filter_by_state(items, state):
    """Фильтрует список словарей по заданному статусу."""
    if not isinstance(items, list):
        raise ValueError("Входные данные должны быть списком")

    return [item for item in items if item.get('state') == state]


def sort_by_date(items, reverse=False):
    if not isinstance(items, list):
        raise ValueError("Входные данные должны быть списком")

    # Определяем форматы данных для сопоставления
    date_formats = [
        "%Y-%m-%d",  # Год-месяц-день
        "%d-%m-%Y",  # День-месяц-год
        "%m/%d/%Y",  # Месяц/день/год
        "%Y/%m/%d",  # Год/месяц/день
        "%d %B %Y",  # День Месяц Год
        "%B %d, %Y"  # Месяц День, Год
    ]

    for item in items:
        date_str = item.get('date')
        if not date_str:
            raise ValueError("Отсутствует дата в одном из словарей")

        # Попытка преобразовать дату с помощью всех форматов
        for fmt in date_formats:
            try:
                item['parsed_date'] = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Некорректный формат даты: {date_str}")

    # Сортируем по проверенной дате
    return sorted(items, key=lambda x: x['parsed_date'], reverse=reverse)

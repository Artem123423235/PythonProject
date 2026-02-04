def divide(a, b):
    return a / b


from datetime import datetime

def sort_by_date(items, reverse=False):
    """Сортирует список словарей по дате."""
    if not isinstance(items, list):
        raise ValueError("Входные данные должны быть списком")

    date_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d %B %Y",
        "%B %d, %Y"
    ]

    for item in items:
        date_str = item.get('date')
        if not date_str:
            raise ValueError("Отсутствует дата в одном из словарей")

        for fmt in date_formats:
            try:
                item['parsed_date'] = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Некорректный формат даты: {date_str}")

    return sorted(items, key=lambda x: x['parsed_date'], reverse=reverse)


def filter_by_state(items, state):
    """Фильтрует список словарей по заданному статусу."""
    if not isinstance(items, list):
        raise ValueError("Входные данные должны быть списком")

    return [item for item in items if item.get('state') == state]

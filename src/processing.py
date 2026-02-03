# src/processing.py

def filter_by_state(data, state='EXECUTED'):
    """
    Функция для фильтрации списка словарей по значению ключа 'state'.

    :param data: Список словарей
    :param state: Значение для фильтрации (по умолчанию 'EXECUTED')
    :return: Новый список словарей, удовлетворяющих условию
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data, descending=True):
    """
    Функция для сортировки списка словарей по дате.

    :param data: Список словарей
    :param descending: Порядок сортировки (по умолчанию True - убывание)
    :return: Новый отсортированный список
    """
    return sorted(data, key=lambda x: x['date'], reverse=descending)

def divide(a, b):
    return a / b
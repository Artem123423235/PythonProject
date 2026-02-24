import requests

def get_currency_rate(currency_code):
    """Получает курс валюты по отношению к рублю."""
    url = f"https://api.exchangerate-api.com/v4/latest/{currency_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "RUB" in data["rates"]:
            return data["rates"]["RUB"]
        else:
            raise ValueError("Курс для RUB не найден.")
    else:
        raise ValueError("Не удалось получить курс валюты.")

def convert_to_rub(transaction):
    """
    Принимает транзакцию и возвращает сумму в рублях.

    :param transaction: Словарь с данными транзакции.
    :return: Сумма транзакции в рублях (float).
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except KeyError as e:
        raise ValueError("Некорректная структура транзакции.") from e
    except ValueError as e:
        raise ValueError("Некорректный формат суммы.") from e

    if currency_code == "RUB":
        return amount
    elif currency_code in ["USD", "EUR"]:
        rate = get_currency_rate(currency_code)
        return amount * rate
    else:
        raise ValueError("Неподдерживаемая валюта.")

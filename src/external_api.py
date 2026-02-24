import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data"
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными о транзакции (должен содержать ключи 'amount' и 'currency')
    :return: Сумма транзакции в рублях
    :raises ValueError: Если валюта недействительна или если отсутствуют необходимые ключи
    """
    # Проверка наличия необходимых ключей
    if "amount" not in transaction or "currency" not in transaction:
        raise ValueError("Transaction must contain 'amount' and 'currency' keys")

    amount = transaction["amount"]
    currency = transaction["currency"]

    # Проверка, является ли валюта рублем
    if currency == "RUB":
        return float(amount)

    # Запрос на получение курса валют
    response = requests.get(f"{API_URL}/latest?base={currency}", headers={"apikey": API_KEY})
    data = response.json()

    # Проверка наличия ошибки в ответе
    if "error" not in data:
        exchange_rate = data["rates"].get("RUB")
        if exchange_rate is not None:
            return float(amount) * exchange_rate

    raise ValueError("Invalid currency or conversion error")
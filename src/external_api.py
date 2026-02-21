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

    :param transaction: Словарь с данными о транзакции (содержит ключи 'amount' и 'currency')
    :return: Сумма транзакции в рублях
    :raises ValueError: Если валюта недействительна
    """
    amount = transaction["amount"]
    currency = transaction["currency"]

    if currency == "RUB":
        return float(amount)

    response = requests.get(f"{API_URL}/latest?base={currency}", headers={"apikey": API_KEY})
    data = response.json()

    if "error" not in data:
        exchange_rate = data["rates"]["RUB"]
        return float(amount) * exchange_rate

    raise ValueError("Invalid currency or conversion error")

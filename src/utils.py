import json
import os
from decorators.log import setup_logger

logger = setup_logger('utils')


def utils_function():
    try:
        logger.info("Функция utils_function запущена.")

        # Логика функции...

        logger.info("Функция utils_function успешно завершена.")
    except Exception as e:
        logger.error(f"Ошибка в функции utils_function: {e}")

def load_transactions(file_path):
    """
    Читает JSON-файл и возвращает список транзакций.

    :param file_path: Путь к JSON-файлу
    :return: Список словарей с данными о транзакциях или пустой список
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

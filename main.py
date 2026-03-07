import os
import json
from data_loader import load_csv_transactions, load_excel_transactions  # Импорт функций
from src.masks import load_transactions  # Импортируем правильно из src.masks
from search import process_bank_search, process_bank_operations  # Импорт новых функций


def format_transaction(transaction):
    """
    Форматирует транзакцию в удобный для отображения вид.
    """
    if transaction['state'].upper() == 'EXECUTED':
        date = transaction['date'][:10]  # Отрезаем время, оставляем только дату
        description = transaction['description']

        # Обработка сумм и валюты в зависимости от структуры данных
        if 'operationAmount' in transaction:
            amount = transaction['operationAmount']['amount']
            currency = transaction['operationAmount']['currency']['name']
        else:
            amount = transaction.get('amount')  # Обработаем CSV или XLSX
            currency = transaction.get('currency_name')  # В случае, если мы из CSV

        # Формирование строки транзакции
        account_from = transaction.get('from', 'Не указано')
        account_to = transaction.get('to', 'Не указано')
        return f"{date} {description}\nСчет: {account_from}\nСумма: {amount} {currency}\n"

    return None


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    data = []  # Инициализируем переменную для хранения данных

    if choice == "1":
        json_file_path = 'transactions.json'  # Указываем путь к JSON файлу
        if os.path.exists(json_file_path):
            data = load_transactions(json_file_path)  # Используем функцию, которая загружает данные из JSON
        else:
            print(f"JSON файл '{json_file_path}' не найден.")
            return
    elif choice == "2":
        csv_file_path = 'transactions.csv'  # Указываем путь к файлу CSV
        if os.path.exists(csv_file_path):
            data = load_csv_transactions(csv_file_path)
        else:
            print(f"CSV файл '{csv_file_path}' не найден.")
            return
    elif choice == "3":
        xlsx_file_path = 'transactions_excel.xlsx'  # Указываем путь к файлу XLSX
        if os.path.exists(xlsx_file_path):
            data = load_excel_transactions(xlsx_file_path)
        else:
            print(f"XLSX файл '{xlsx_file_path}' не найден.")
            return
    else:
        print("Неверный выбор.")
        return

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status = input(
        "Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): ").strip().upper()

    while status not in valid_statuses:
        print(f'Статус операции "{status}" недоступен.')
        state = input(
            "Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): ").strip().upper()

    print(f'Операции отфильтрованы по статусу "{status}".')

    # Фильтрация по статусу, для JSON необходимо проверить на соответствие 'state'
    filtered_data = [transaction for transaction in data if str(transaction.get('state', '')).upper() == status]

    if not filtered_data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    sort_order = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_order == "да":
        order = input("Сортировать по возрастанию или по убыванию? (возрастанию/убыванию): ").strip().lower()
        if order == "возрастанию":
            filtered_data.sort(key=lambda x: x['date'])
        elif order == "убыванию":
            filtered_data.sort(key=lambda x: x['date'], reverse=True)

    currency_filter = input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower()
    if currency_filter == "да":
        filtered_data = [transaction for transaction in filtered_data if
                         transaction.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB']

    description_search = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if description_search == "да":
        search_str = input("Введите строку для поиска: ")
        filtered_data = process_bank_search(filtered_data, search_str)

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_data)}")

    for transaction in filtered_data:
        formatted_transaction = format_transaction(transaction)
        if formatted_transaction:
            print(formatted_transaction)


if __name__ == '__main__':
    main()

from decorators import log  # Предполагается, что декораторы находятся в decorators.py
# Импорт функций
import pandas as pd
from data_loader import load_csv_transactions, load_excel_transactions  # Импорт функций
from search import process_bank_search, process_bank_operations  # Импорт новых функций
import json

# Считываем данные из CSV-файла
csv_file_path = 'transactions.csv'  # Укажите путь к CSV файлу
transactions_csv = load_csv_transactions(csv_file_path)  # Загружаем CSV данные

# Выводим первые 5 строк для проверки
print("Данные из CSV:")
print(transactions_csv[:5])  # Вывод первых 5 строк как список словарей

# Считываем данные из XLSX-файла
xlsx_file_path = 'transactions_excel.xlsx'  # Укажите путь к XLSX файлу
transactions_xlsx = load_excel_transactions(xlsx_file_path)  # Загружаем XLSX данные

# Выводим первые 5 строк для проверки
print("Данные из XLSX:")
print(transactions_xlsx[:5])  # Вывод первых 5 строк как список словарей


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


my_function(1, 2)


@log()
def my_function_with_error(x: int, y: int) -> int:
    return x / y


try:
    my_function_with_error(1, 0)
except ZeroDivisionError:
    pass


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    if choice == "1":
        with open('transactions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif choice == "2":
        file_path = 'transactions.csv'
        data = load_csv_transactions(file_path)
    elif choice == "3":
        file_path = 'transactions_excel.xlsx'
        data = load_excel_transactions(file_path)
    else:
        print("Неверный выбор.")
        return

    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']
    status = input("Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): ").strip().upper()

    while status not in valid_statuses:
        print(f'Статус операции "{status}" недоступен.')
        status = input("Введите статус, по которому необходимо выполнить фильтрацию (EXECUTED, CANCELED, PENDING): ").strip().upper()

    print(f'Операции отфильтрованы по статусу "{status}".')

    # Фильтрация по статусу
    filtered_data = [transaction for transaction in data if transaction.get('state', '').upper() == status]

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
        filtered_data = [transaction for transaction in filtered_data if transaction.get('currency') == 'RUB']

    description_search = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").strip().lower()
    if description_search == "да":
        search_str = input("Введите строку для поиска: ")
        filtered_data = process_bank_search(filtered_data, search_str)

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_data)}")

    for transaction in filtered_data:
        print(f"{transaction['date']} {transaction['description']}")
        print(f"Счет: {transaction.get('account')}")
        print(f"Сумма: {transaction.get('amount')} {transaction.get('currency')}")
        print()  # Для разделения


if __name__ == '__main__':
    main()

import os
import json
from data_loader import load_csv_transactions, load_excel_transactions  # Импорт функций
from search import process_bank_search, process_bank_operations  # Импорт новых функций

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ")

    data = []  # Инициализируем переменную для хранения данных

    if choice == "1":
        if os.path.exists('transactions.json'):
            with open('transactions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            print("JSON файл 'transactions.json' не найден.")
            return
    elif choice == "2":
        if os.path.exists('transactions.csv'):
            file_path = 'transactions.csv'
            data = load_csv_transactions(file_path)
        else:
            print("CSV файл 'transactions.csv' не найден.")
            return
    elif choice == "3":
        if os.path.exists('transactions_excel.xlsx'):
            file_path = 'transactions_excel.xlsx'
            data = load_excel_transactions(file_path)
        else:
            print("XLSX файл 'transactions_excel.xlsx' не найден.")
            return
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

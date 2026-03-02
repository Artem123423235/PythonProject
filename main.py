from decorators import log  # Предполагается, что декораторы находятся в decorators.py
from data_loader import load_csv_transactions, load_excel_transactions  # Импорт функций
import pandas as pd

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

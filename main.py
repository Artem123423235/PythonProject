from PythonProject.decorators import log
import pandas as pd

# Считываем данные из CSV-файла
csv_file_path = 'transactions.csv'  # Укажите путь к CSV файлу
transactions_csv = pd.read_csv(csv_file_path)  # Считываем CSV данные

# Выводим первые 5 строк для проверки
print("Данные из CSV:")
print(transactions_csv.head())

# Считываем данные из XLSX-файла
xlsx_file_path = 'transactions_excel.xlsx'  # Укажите путь к XLSX файлу
transactions_xlsx = pd.read_excel(xlsx_file_path)  # Считываем XLSX данные

# Выводим первые 5 строк для проверки
print("Данные из XLSX:")
print(transactions_xlsx.head())


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
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# main.py

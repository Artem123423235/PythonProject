# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
def calculate_logarithm(x, base):
    return math.log(x, base)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def add_numbers(a, b):
    return a + b


def is_even(a):
    return a % 2 == 0


def find_max(my_list):
    if len(my_list) > 0:
       return max(my_list)
    return 0

if __name__ != '__main__':
    pass
else:
    assert add_numbers(2, 2) == 4

    assert is_even(add_numbers(2, 2)) == True

    assert find_max([1, 2, 3, 4, 5]) == 5

    assert find_max([]) == 0


    def divide(a, b):
        if b > 0:
            return a / b
        return 0



import numpy as np
from PIL import Image
from cmath import *
from prettytable import PrettyTable

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def create_array(arr):
    array = []
    size = 64
    for i in range(size):
        for j in range(size):
            array.append(arr[i][j][0])
    return array

def correlation(first, second):
    sum_first = 0
    sum_second = 0
    for i in range(4096):
        sum_first += first[i]
        sum_second += second[i]
    avg_first = sum_first/4096
    avg_second = sum_second/4096
    up = 0
    down_first = 0
    down_second = 0
    down = 0
    for j in range(4096):
        up += (first[j] - avg_first) * (second[j] - avg_second)
        down_first += (first[j] - avg_first) * (first[j] - avg_first)
        down_second += (second[j] - avg_second) * (second[j] - avg_second)
    down = sqrt(down_first * down_second)
    coef = up / down
    return coef


def autocorrrelation(array):
    up = 0
    down = 0
    avg = 0
    for coef in range(len(array)):
        for i in range(len(array)):
            if i - coef >= 0:
                up += int(array[i])*int(array[i-coef])
        avg += up
        up = 0
    avg = avg / len(array)
    up = avg
    for i in range(len(array)):
        down += int(array[i])*int(array[i])
    result = up/down
    return result

def do_aut(list):
    table_row = []
    table = PrettyTable()
    table.field_names = list
    for i in list:
        img_first = Image.open(f'Photo/{i}.png')
        arr = np.asarray(img_first, dtype='uint8')
        array_first = create_array(arr)
        result = autocorrrelation(array_first)
        table_row.append(toFixed(result.real, 2))
    table.add_row(table_row)
    print(table)

def do_cor(list1, list2):
    table_fields = ['']
    if len(list1) > len(list2):
        for i in list1:
            table_fields.append(i)
    else:
        for i in list2:
            table_fields.append(i)
        swap = list1
        list1 = list2
        list2 = swap
    table_row = []
    table = PrettyTable()
    table.field_names = table_fields
    for i in list2:
        table_row.append(i)
        img_first = Image.open(f'Photo/{i}.png')
        arr = np.asarray(img_first, dtype='uint8')
        array_first = create_array(arr)
        for j in list1:
            img_first = Image.open(f'Photo/{j}.png')
            arr = np.asarray(img_first, dtype='uint8')
            array_second = create_array(arr)
            result = correlation(array_first, array_second)
            table_row.append(toFixed(result.real, 2))
            if float(toFixed(result.real, 2)) >0.5 and float(toFixed(result.real, 2)) < 1:
                print(f"Між {i} та {j} знайдено великий коефіцієнт: {toFixed(result.real, 2)}")
        table.add_row(table_row)
        table_row = []
    print(table)

list_numbers = [
     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]
list_small = [
    'а', 'б', 'в', 'г', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я'
]
list_big = [
    'Ав', 'Бв', 'Вв', 'Гв', 'Дв', 'Ев', 'Єв', 'Жв', 'Зв', 'Ив', 'Ів', 'Їв', 'Йв', 'Кв', 'Лв', 'Мв', 'Нв', 'Ов', 'Пв', 'Рв', 'Св', 'Тв', 'Ув', 'Фв', 'Хв', 'Цв', 'Чв', 'Шв', 'Щв', 'Ьв', 'Юв', 'Яв'
]

while 0 == 0:
    print("1. Автокореляція\n2. Взаємна кореляція")
    choice1 = input("Оберіть вид кореляції: ")
    if choice1 == "1":
        print("1. 0-9\n2. а-я\n3. А-Я")
        choice2 = input("Оберіть символи для автокореляції: ")
        if choice2 == "1":
            do_aut(list_numbers)
        elif choice2 == "2":
            do_aut(list_small)
        else:
            do_aut(list_big)
    else:
        print("1. 0-9\n2. а-я\n3. А-Я")
        choice3 = input("Оберіть перший набір симворів для взаємної кореляції: ")
        choice4 = input("Оберіть другий набір симворів для взаємної кореляції: ")
        if choice3 == "1" and choice4 == "1":
            do_cor(list_numbers, list_numbers)
        if choice3 == "1" and choice4 == "2":
            do_cor(list_numbers, list_small)
        if choice3 == "1" and choice4 == "3":
            do_cor(list_numbers, list_big)
        if choice3 == "2" and choice4 == "2":
            do_cor(list_small, list_small)
        if choice3 == "2" and choice4 == "3":
            do_cor(list_small, list_big)
        if choice3 == "3" and choice4 == "3":
            do_cor(list_big, list_big)

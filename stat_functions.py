from settings import stat_file_name
import csv
from Enemies import *


# обновление статистики, запись необходимых данных в csv файл. только в режиме нонстопа
# запись данных при происшествии определенного события, анализ флагов
def review_stats(file_name, enemy=None, killed=False, time_ticked=False, shoted=False):
    global headers
    if killed:
        if type(enemy) == Villager:
            change_col = headers[0]
        elif type(enemy) == Musketeer:
            change_col = headers[1]
        elif type(enemy) == Magician:
            change_col = headers[2]
    elif shoted:
        change_col = headers[4]
    elif time_ticked:
        change_col = headers[5]

    # считываем текущие данные, сохраняем построчно в дату. создаем новую строчку произошедшего события
    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
        new_row = {k: int(v) + 1 if k == change_col else v for k, v in data[len(data) - 1].items()}
        if killed:
            new_row = {k: int(v) + 1 if k == headers[3] else v for k, v in new_row.items()}
        data.append(new_row)
    # записываем файл заново. текущие данные + новая строчка события
    with open(stat_file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# получить словарь данных из csv файла статистики
def stat_results(file_name):
    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
    return data[-1].items()


# начать, создать файл статистики
def start_stats(file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers,
                                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        start_data = {}
        for header, start_vals in zip(headers, [0] * len(headers)):
            start_data[header] = start_vals
        writer.writerow(start_data)

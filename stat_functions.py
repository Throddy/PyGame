from settings import stat_file_name
from Enemies import *


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

    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
        new_row = {k: int(v) + 1 if k == change_col else v for k, v in data[len(data) - 1].items()}
        if killed:
            new_row = {k: int(v) + 1 if k == headers[3] else v for k, v in new_row.items()}
        data.append(new_row)

    with open(stat_file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def stat_results(file_name):
    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
    return data[-1].items()

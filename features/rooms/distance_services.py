import pprint
from os import path

import numpy as np
import openpyxl
import pandas as pd


def read_distances():
    file_path = path.join(path.dirname(path.abspath(__file__)), '../../data')
    data = []
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test.xlsx')
    raw_data = pd.read_excel(file_path + '/exam_input_data_test.xlsx', sheet_name='distances')
    # print(raw_data.to_dict('record'))
    for row in raw_data.to_dict('record'):
        data.append(
            tuple((value for value in row.values() if not pd.isna(value))))
    # formatted_data = list(data[2:])
    columns = [item for item in data[1][1:]]
    rows = [item for item in data[2:]]
    ls = []
    for i in range(len(columns)):
        for j in range(len(rows)):
            dic = {
                'Distance': rows[j][i+1],
                'Destination': columns[i],
                'Origin': rows[j][0]
            }
            ls.append(dic)
    for distance in ls:
        distance['Distance'] /= 1000

    return ls


def get_distance_between_rooms(roomA, roomB):
    ls = read_distances()
    return [room['Distance'] for room in ls if room['Destination'] in roomA and room['Origin'] in roomB]


def find_average_distance(rooms):
    distances = []
    for i in range(0, len(rooms)):
        distances.append(get_distance_between_rooms(rooms[i-1], rooms[i])[0])
    return (sum(distances[1:])/len(rooms))


if __name__ == "__main__":

    # ls = read_distances()
    # roomA = 'NB'
    # roomB = 'OLD'

    # distnce = get_distance_between_rooms(roomA, roomB)
    # actual_distance = distnce[0]
    # print(actual_distance)
    # if 0.1 <= actual_distance <= 1.0:
    #     print(2)
    # elif 1.1 <= actual_distance <= 2.0:
    #     print(4)
    # elif 2.1 <= actual_distance <= 5.0:
    #     print(7)

    roomA = ['EHC_101', 'NB_232', 'OLD_21', 'EHC_212', 'EHC_212', 'EHC_232', 'NB_232']
    roomB = ['NB_232', 'EHC_212', 'EHC_232', 'NB_232']
    pprint.pprint(get_distance_between_rooms(roomA[0], roomA[1]))
    # print(len(roomA))
    # print(find_average_distance(roomA))
    print(find_average_distance(roomB))

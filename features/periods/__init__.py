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
    return ls


def get_rooms_in_EHC(room):
    if s.startswith('E'):
        return true


if __name__ == "__main__":

    # dict = read_distances()

    # pprint.pprint(dict)
    print(get_rooms_in_EHC('OLD'))

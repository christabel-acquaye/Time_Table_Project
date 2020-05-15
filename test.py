import openpyxl
from os import path
import pandas as pd
import numpy as np




def read_distances():
    file_path = path.join(path.dirname(path.abspath(__file__)), 'data')
    data = []
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test.xlsx')
    raw_data = pd.read_excel(file_path + '/exam_input_data_test.xlsx', sheet_name='distances')
    # print(raw_data.to_dict('record'))
    for row in raw_data.to_dict('record'):
        data.append(
        tuple((value for value in row.values() if not pd.isna(value))))
    formatted_data = list(data[2:])
    print(formatted_data)
    return data


if __name__ == "__main__":
    read_distances()
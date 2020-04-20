import openpyxl
from os import path
import pandas as pd

from features.exam.services import insert_exam
from features.rooms.services import insert_rooms
from features.periods.services import insert_period


def read_exam(insert = False):
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    print(file_path)
    book = openpyxl.load_workbook(file_path + '/exam_input_data.xlsx')
    exam_data = pd.read_excel(file_path + '/exam_input_data.xlsx', sheet_name='exams')
    print(room_data.to_dict('record'))
    # print(exam_data.to_dict('record'))

    normalized_data = []

    for data in exam_data.to_dict('record'):
        item = {
            'id' : data['ExamID'],
            'length': data['Length'] ,
            'alt': data['Alt_Seating'],
            'minSize' : data['MinSize'],
            'maxRooms' : data['MaxRooms'],
            'average' : data['Average'],
            'examCode' : data['ExamCode']
        }
        normalized_data.append(item)
        if insert:
            insert_exam(**item)
        print(data)

    return normalized_data


def read_room(insert = False):
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    print(file_path)
    book = openpyxl.load_workbook(file_path + '/exam_input_data.xlsx')
    room_data = pd.read_excel(file_path + '/exam_input_data.xlsx', sheet_name='rooms')
    print(room_data.to_dict('record'))

    normalized_data = []
    for data in room_data.to_dict('record'):


        item = {
            'id' : data['RoomID'],
            'roomName': data['RoomName'] ,
            'alt': data['Alt_Size'],
            'size' : data['Size'],
            'coord_longitude' : data['Coord_Longitude'],
            'coord_latitude' : data['Coord_Latitude'],

        }
        normalized_data.append(item)
        if insert:
            insert_rooms(**item)
        print(data)

    return normalized_data



def read_period(insert = False):
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    print(file_path)
    book = openpyxl.load_workbook(file_path + '/exam_input_data.xlsx')
    period_data = pd.read_excel(file_path + '/exam_input_data.xlsx', sheet_name='periods')
    print(period_data.to_dict('record'))

    normalized_data = []

    for data in period_data.to_dict('record'):
        item = {
            'id' : data['PeriodID'],
            'length': data['Length'] ,
            'day': data['Date'],
            'time' : data['Time'],
            'penalty' : data['Penalty']

        }
        normalized_data.append(item)
        if insert:
            insert_period(**item)
        print(data)

    return normalized_data




if __name__ == '__main__':
    read_period()
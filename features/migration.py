import pprint
from os import path

import openpyxl
import pandas as pd
from openpyxl import Workbook, load_workbook

from features.exam.service import insert_exam
from features.miscellaneous_functions import read_period_data
from features.periods.service import insert_period
from features.rooms.service import insert_rooms


def insert_into_excel(row, column, data):
    book = Workbook()
    sheet = book.active
    sheet.cell(row=row, column=column).value = data
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data/input_data.xlsx')
    book.save(file_path)


def read_exam(insert=False):
    '''
    Function that reads the details from the excel file and inserts them into the exams table
    '''

    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    exam_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='exams')

    normalized_data = []

    for data in exam_data.to_dict('record'):
        item = {
            'id': data['ExamID'],
            'length': data['Length'],
            'alt': data['Alt_Seating'],
            'minSize': data['MinSize'],
            'maxRooms': data['MaxRooms'],
            'average': data['Average'],
            'examCode': data['ExamCode']
        }
        normalized_data.append(item)
        if insert:
            insert_exam(**item)

    return normalized_data


def read_room(insert=False):
    '''
    Function that reads the details from the excel file and inserts them into the room table
    '''

    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    room_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='rooms')

    normalized_data = []
    for data in room_data.to_dict('record'):

        item = {
            'id': data['RoomID'],
            'roomName': data['RoomName'],
            'alt': data['Alt_Size'],
            'size': data['Size'],
            'coord_longitude': data['Coord_Longitude'],
            'coord_latitude': data['Coord_Latitude'],

        }
        normalized_data.append(item)
        if insert:
            insert_rooms(**item)

    return normalized_data


def read_period(insert=False):
    '''
    Function that reads the details from the excel file and inserts them into the periods table
    '''

    period_data = read_period_data()
    normalized_data = []

    for index, data in enumerate(period_data):
        item = {
            'id': index + 1,
            'length': data['length'],
            'day': data['date'],
            'time': data['time'],
            'penalty': data['penalty']

        }
        normalized_data.append(item)
        if insert:
            insert_period(**item)

    return normalized_data


def read_student():
    '''
    Function that reads the details from the excel file and organizes it in a more usable form
    '''

    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    student_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='students')

    student_group = []
    for data in student_data.to_dict('record'):
        item = list(data.values())
        dic = {
            'id': item[0],
            'course': item[1:]
        }

        flipped = []

        for course in dic['course']:
            if course not in flipped:
                flipped.append(course)
        dic['course'] = flipped
        student_group.append(dic)

    return student_group


def read_room_preference():
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    room_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='room_preference')
    room_preference = []
    for data in room_data.to_dict('record'):
        item = {
            'examCode': data['ExamCode'],
            'roomName': data['RoomName']

        }
        room_preference.append(item)
    return room_preference


def read_precedence():
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    precedence_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='precedence')
    normalized_data = []
    for data in precedence_data.to_dict('record'):
        item = {
            'examCode': data['ExamCode'],
            'precedence': data['Precedence']

        }
        normalized_data.append(item)
    return normalized_data


def read_period_preference():
    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    period_preference_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='period_preference')
    normalized_data = []
    for data in period_preference_data.to_dict('record'):
        item = {
            'examCode': data['ExamCode'],
            'date': data['Date'],
            'time': data['Time']

        }
        normalized_data.append(item)
    return normalized_data


if __name__ == "__main__":
    from main import app
    with app.app_context():
        read_exam(insert = True)
        read_room(insert = True)
        read_period(insert = True)
        read_period_preference()
        read_precedence()
        read_room_preference()
        read_student()
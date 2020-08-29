import datetime
import math
import pprint
import time
from os import path

import openpyxl
import pandas as pd
from openpyxl import Workbook, load_workbook


def read_input():

    file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
    book = openpyxl.load_workbook(file_path + '/exam_input_data_test_01.xlsx')
    input_data = pd.read_excel(file_path + '/exam_input_data_test_01.xlsx', sheet_name='inputs')

    output_dic = {}
    for data in input_data.to_dict('record'):
        # print(data)
        output_dic[data['Variable']] = data['Value']
    return output_dic


def get_date_input(date_entry):
    print(date_entry)
    day, month, year = map(int, date_entry.split('/'))
    print(year, month, day)
    return datetime.date(year, month, day)


# end_date = start_date + datetime.timedelta(days=14)
def get_period_date(start_date, end_date):

    date_generated = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days + 1)]
    formatted_data = [data.strftime("%Y,%m,%d") for data in date_generated]
    exam_dates = []
    for date_date in formatted_data:
        res = tuple(map(int, date_date.split(',')))
        today = datetime.datetime(res[0], res[1], res[2])
        weekno = today.weekday()
        if weekno < 5:
            year, month, day = map(int, date_date.split(','))
            formated_date = datetime.date(year, month, day)
            exam_dates.append(formated_date.strftime('%d/%m/%Y'))
    return exam_dates


def get_exam_stop_date(start_hour, start_minute, duration):
    start = datetime.datetime(100, 1, 1, start_hour, start_minute, 0)
    end = start + datetime.timedelta(minutes=duration)
    return start, end


def add_break(time):
    return time + datetime.timedelta(minutes=30)


def get_period_list(start_date, stop_date, duration, periods_per_day):
    date_data = get_period_date(start_date, stop_date)
    period_list = []
    for data in date_data:
        for i in range(0, periods_per_day):
            start_time, end_time = 0, 0
            if i == 0:
                start, end = get_exam_stop_date(8, 00, duration)
                time = str(start.time()) + '-' + str(end.time())

            else:
                start = add_break(end)
                start, end = get_exam_stop_date(start.hour, start.minute, duration)
                time = str(start.time()) + '-' + str(end.time())
            dic = {
                'length': duration,
                'date': data,
                'time': time,
                'penalty': 0
            }
            period_list.append(dic)
    return period_list


def get_date_difference(date1, date2):
    date1 = datetime.datetime.strptime(date1, "%Y-%d-%m %H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%Y-%d-%m %H:%M:%S")
    return abs((date2 - date1).days)


def has_same_date(date1, date2):
    # print('Test  dates', date1, type(date1))

    date1 = datetime.datetime.strptime(date1, '%Y-%d-%m %H:%M:%S') if isinstance(date1, str) else date1
    # date1 = datetime.datetime.strptime(date1, "%Y-%d-%m %H:%M:%S")
    # date2 = datetime.datetime.strptime(date2, "%Y-%d-%m %H:%M:%S")
    date1 = datetime.datetime.strptime(date2, '%Y-%d-%m %H:%M:%S') if isinstance(date2, str) else date2
    if date1 != date2:
        return True
    return False


def read_period_data():
    data = read_input()
    start_date = pd.to_datetime(data['Start_Date(dd/mm/yyyy)'], format='%Y-%m-%d')

    dt = start_date.date()
    start_date = datetime.datetime(dt.year, dt.day, dt.month, 0, 0, 0)
    end_date = pd.to_datetime(data['Stop_Date(dd/mm/yyyy)'], format='%Y-%m-%d')
    dt1 = end_date.date()
    end_date = datetime.datetime(dt1.year, dt1.day, dt1.month, 0, 0, 0)
    duration = data['Exam_Duration(mins)']
    print(duration)
    periods_per_day = data['Periods_In_Day']
    print(periods_per_day)
    return get_period_list(start_date, end_date, duration, periods_per_day)


if __name__ == "__main__":

    # start_date = get_date_input()
    # stop_date = get_date_input()
    # duration = int(input("Duration:\t"))
    # data = get_period_list(start_date, stop_date, duration)
    # pprint.pprint(data)
    # pprint.pprint(len(data))
    # f_date = '2020-04-05 00:00:00'
    # l_date = '2020-04-05 00:00:00'
    # print(has_same_date(f_date, l_date))
    # raw = '2020-04-05 00:00:00'
    # print(Timestamp.valueof(raw))
    # print(get_date_input(datetime(raw)))
    pprint.pprint(read_period_data())
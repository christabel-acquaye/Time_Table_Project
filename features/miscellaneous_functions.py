
import datetime
import pprint

import pandas as pd


def get_date_input():
    date_entry = input('Enter a date in YYYY-MM-DD format:\t')
    year, month, day = map(int, date_entry.split('-'))
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


def get_period_list(start_date, stop_date, duration):
    date_data = get_period_date(start_date, stop_date)
    period_list = []
    for data in date_data:
        for i in range(0, 3):
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


if __name__ == "__main__":

    start_date = get_date_input()
    stop_date = get_date_input()
    duration = int(input("Duration:\t"))
    data = get_period_list(start_date, stop_date, duration)
    pprint.pprint(data)
    pprint.pprint(len(data))

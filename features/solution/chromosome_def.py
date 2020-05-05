

import datetime
import openpyxl
from os import path
import pandas as pd
from features.periods.services import get_period_bound
from features.exam.services import get_exam_bound
from  features.solution.services import rand_gen
# file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
# print(file_path)
# book = openpyxl.load_workbook(file_path + '/exam_input_data.xlsx')
# student_data = pd.read_excel(file_path + '/exam_input_data.xlsx', sheet_name='students')


# exam_count = -1
# for i in student_data.columns:
#     exam_count += 1

# print(exam_count)
# user_input = str(input('Enter Start Date for exam (i.e 2019, 06, 29):\t'))
# year, month, day = map(int, user_input.split(','))
# exam_start_date = datetime.datetime(year, month, day)
# # exam_start_date = datetime.datetime.now()
# print(exam_start_date)
# exam_per_day = 1
# days_period = exam_count / exam_per_day
# end_date = exam_start_date + datetime.timedelta(days=days_period)
# print(end_date)

# # periods[(days_period*exam_per_day)]


def chromosome_assignment(period, rooms_avaliable, exam):
    chromosome = []
    period_finsih = get_period_bound() + 1 
    period = list(range(1,period_finsih))
    exam_finish = get_exam_bound() + 1
    exam = rand_gen(1, exam_finish)
    period_exam_assignment = dict(zip(period, exam))
    print(period_exam_assignment)
  


if __name__ == "__main__":
    chromosome_assignment(2, 2,23)
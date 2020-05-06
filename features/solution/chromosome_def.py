

import datetime
import openpyxl
from os import path
import pandas as pd
from features.periods.services import get_period_bound
from features.exam.services import get_exam_bound
from  features.solution.services import rand_gen
import pprint
from features.solution.rooomAssign import period_room_allocation, room_compute
from features.solution.examAssign import period_exam_allocation
from features.exam.services import get_exam, get_exam_column
from features.periods.services import get_period
from features.rooms.services import get_rooms
import random
import json

# file_path = path.join(path.dirname(path.abspath(__file__)), '../data')
# print(file_path)
# book = openpyxl.load_workbook(file_path + '/exam_input_data.xlsx')
# student_data = pd.read_excel(file_path + '/exam_input_data.xlsx', sheet_name='students')


# exam_count = -1
# for i in student_data.columns:get_exam_column(cur, columnName, id=None)
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


def format_rooms(rooms):
    return [{'name': room[1], 'no_of_stds': room[2]} for room in rooms]


def chromosome():
    exams = get_exam()
    
    period_finsih = get_period_bound() 
    period_room= period_room_allocation(get_period(), get_rooms())
  
    # print(ran_period)
    period_exams =[]
    count = 0
    for exam in exams:
        # pprint.pprint(type(exam[3]))
        ran_period = random.randint(1, period_finsih)
        room_allocated, available_rooms =  room_compute(exam[3], period_room[ran_period - 1])
        
        period_room[ran_period - 1] = available_rooms
        # print('\trooms allocated', format_rooms(room_allocated)) 
        # print('\tstudents with seats', sum([ room[1] for room in format_rooms(room_allocated)]) )
        std_with_seats = sum([ room['no_of_stds'] for room in format_rooms(room_allocated)])
        if not std_with_seats == exam[3]:
            print('period', ran_period, 'exam', exam[0], 'std_size', exam[3])
            print("\tsome students didn't get seats, std_with_seats: %s, std_size: %s " (std_with_seats, exam[3]))

        period_exam_assignment = {
            'period_id' : ran_period,
            'exam_id' : exam[0], 
            'rooms': format_rooms(room_allocated) 
        }
        period_exams.append(period_exam_assignment)

    pprint.pprint(period_exams, indent=1) # I owe you food okay and 50 dancing emojis...I want pizza..I will buy it ..When i come. yayyy
    # left foot up, right foot slide
    # vhom..Im danicng here..Thank you sooooooooooooooooo much

    return period_exams


if __name__ == "__main__":
    population_size = int(input('Population Size: \t'))
    generated_chromosome = [chromosome() for i in range(population_size)]
    
    with open('population.json', 'w') as file:
        json.dump(generated_chromosome, file, indent=1)
        
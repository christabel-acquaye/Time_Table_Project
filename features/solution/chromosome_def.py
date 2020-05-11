

import datetime
import openpyxl
from os import path
import pandas as pd
from features.periods.services import get_period_bound
from features.exam.services import get_exam_bound
from  features.solution.services import rand_gen
from features.solution.rooomAssign import period_room_allocation, room_compute
from features.solution.examAssign import period_exam_allocation
from features.exam.services import get_exam, get_exam_column, get_exam_order_by_size
from features.periods.services import get_period
from features.rooms.services import get_rooms
import random
import json
import pprint


def format_rooms(rooms):
    return [{'name': room[1], 'no_of_stds': room[2]} for room in rooms]


def chromosome():
    exams = get_exam_order_by_size()
    
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
            print("\tsome students didn't get seats, std_with_seats: %s, std_size: %s " %(std_with_seats, exam[3])) # problem was over here u forgot the % sign

        period_exam_assignment = {
            'period_id' : ran_period,
            'exam_id' : exam[0], 
            'rooms': format_rooms(room_allocated) 
        }
        period_exams.append(period_exam_assignment)

    # pprint.pprint(period_exams, indent=1)

 
    return period_exams


if __name__ == "__main__":
    population_size = int(input('Population Size: \t'))
    generated_chromosome = [chromosome() for i in range(population_size)]
    pprint.pprint(generated_chromosome)
  
    size = [len(chromosome) for chromosome in generated_chromosome]
    print(size)
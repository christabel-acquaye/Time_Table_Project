import datetime
import json
import pprint
import random
from os import path

import openpyxl
import pandas as pd
from openpyxl import Workbook, load_workbook

from _shared import NotEnoughRooms
from features.exam.service import (get_closed_period, get_exam_bound,
                                   get_exam_column, get_exam_id_from_name,
                                   get_exam_name_from_id,
                                   get_exam_order_by_size, get_exams)
from features.migration import (read_period_preference, read_precedence,
                                read_room_preference)
from features.miscellaneous_functions import get_date_difference
from features.natural_selection.service import (non_dorminating_sort,
                                                over_crowding)
from features.penalty.cost_function import get_fitness_value
from features.periods.service import (check_any_on_same_day, get_period_bound,
                                      get_period_date, get_periods,
                                      get_periods_as_rows_and_columns,
                                      get_periods_with_lengths)
from features.rooms.service import get_rooms
from features.solution.examAssign import period_exam_allocation
from features.solution.roomAssign import period_room_allocation, room_compute
from features.solution.services import rand_gen
from features.students.service import (get_exam_student_group,
                                       get_std_group_with_exams,
                                       get_student_group_exams,
                                       read_student_groups)


def format_rooms(rooms):
    return [{'name': room['roomName'], 'no_of_stds': room['size']} for room in rooms]


def best_fit_exams_in_period(exams, duration):
    """check to see if period duration matches exam duration before assignment

    Arguments:
        exams [list] -- exams
        period duration int -- period duration

    Returns:
       best_fit_exams [list] -- exams whose duration can be accomodated in period's duration
       new_exams_state [list] -- exams whose duration cannot be accomodated in periods duration
     """
    best_fit_exams = []  # exams less than duration
    new_exams_state = []  # exams which do not fit

    for exam in exams:
        if exam['length'] <= duration:
            best_fit_exams.append(exam)
        else:
            new_exams_state.append(exam)

    return best_fit_exams, new_exams_state


def fit_exams_in_rooms(exams, rooms_available, period_id):
    """Fits exams in rooms and returns the exams catered for
    and the pending ones.
    Not all exams can be fitted within the period since we can run
    out of rooms available when fitting the exams

    Arguments:
        exams {list} -- list of exams to attempt fitting
        rooms_available {[dict]} -- list of available rooms
        period_id {[int]} -- period for a particular gene assignment

    Returns:
       period_exams [list] -- periods assigned to exams and rooms
       exams_without_rooms [list] -- exams which size exceeds room availabilty for the particular period
       rooms_available [list] -- rooms available after assignment
    """

    period_exams = []
    exams_without_rooms = []
    for position, exam in enumerate(exams):
        try:
            room_allocated, available_rooms = room_compute(
                exam['minSize'],
                rooms_available[period_id]
            )

            rooms_available[period_id] = available_rooms
            # print('\trooms allocated', format_rooms(room_allocated))
            # print('\tstudents with seats', sum([ room[1] for room in format_rooms(room_allocated)]) )
            std_with_seats = sum(
                [room['no_of_stds']for room in format_rooms(room_allocated)]
            )

            # if not std_with_seats == exam['minSize']:
            # print('period', period_id, 'exam',
            #       exam['id'], 'std_size', exam['minSize'])
            # print("\tsome students didn't get seats, std_with_seats: %s, std_size: %s " % (
            #     std_with_seats, exam['minSize']))

            period_exam_assignment = {
                'period_id': period_id,
                'exam_id': exam['id'],
                'rooms': format_rooms(room_allocated),
                'std_with_seats': std_with_seats
            }
            period_exams.append(period_exam_assignment)
        except NotEnoughRooms:
            # get unassigned exams and send them to a new period
            exams_without_rooms = exams[position:]
            break

    return period_exams, exams_without_rooms, rooms_available


def generate_chromosome():
    """Function that generates multiple genes to form a chromosome
    Arguments:

    Returns:
       chromosome [{list}] --
       [
            {
                "period_id": periods_assigned,
                "exam_id": exams_assigned,
                "rooms": [
                    {
                    "name": name of assigned room,
                    "no_of_stds": no_of_students_that_were_assigned_in_the_room
                    },
            }
        ]
     """
    #  Get exams ordered in descending order of enrollment size
    student_groups = get_std_group_with_exams()  # [ {'student_id: 1, exams: []},{'student_id: 1, exams: []},  ]
    random.shuffle(student_groups)

    periods = get_periods_with_lengths()

    rooms = get_rooms()
    period_rooms = period_room_allocation(periods, rooms)
    exam_no_in_period = [0 for x in range(len(periods))]
    # shuffle periods to add randomization
    random.shuffle(periods)

    # pprint.pprint(periods)
    chromosome = []

    for std in student_groups:
        exams = std['exams']
        exam_periods = []
        current_exam_index = 0

        for period_id, period_duration in periods:
            # get exams with length < length of current period
            # best_fit_exams, next_exams_period = best_fit_exams_in_period(
            #     exams,
            #     period_duration,
            #     period_id
            # )
            max_exams_per_period = 3
            # print('period_id: ', period_id)
            if(current_exam_index + 1 > len(exams)):
                continue

            # if check_any_on_same_day(period_id, exam_periods):
            #     continue
            
            if exam_no_in_period[(period_id - 1)] >= max_exams_per_period:
                continue

            # print('used period_id: ', period_id)
            exam_periods.append(period_id)

            period_exams, exams_without_rooms, period_rooms = fit_exams_in_rooms(
                [exams[current_exam_index]], period_rooms, period_id
            )
            exam_no_in_period[(period_id - 1)] += 1
            current_exam_index += 1

            # prepend unassigned exams to maintain exam order by size
            # exams_without_rooms.extend(next_exams_period)
            # exams = exams_without_rooms
            # print(period_exams)
            chromosome.extend(period_exams)
    # print(periods)
    return chromosome


def generate_population(size):
    """Generates a list of chromosomes based on specified size

    Arguments:
       size int -- number of chromosomes in the population

    Returns:
        A list of chromosomes
     """
    return [generate_chromosome() for i in range(population_size)]


def get_exam_from_gene(chromosome):
    """Filters exam id fonana@christabel-HP-ENVY-x360-m6-Convertible:~/Documents/Professional Projects/TimeTableProject$ git pur every gene in the chromosome
    Arguments:
       chromosome [[list]] -- list of genes

    Returns:
        A list of exam ids in chromosome
     """
    return [gene["exam_id"] for gene in chromosome]


def checkIfDuplicates_1(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


# def a(chromosome):
#     data = [gene['period_id'] for gene in chromosome]
#     dates = [get_period_date(period) for period in data]
#     return checkIfDuplicates_1(dates)


def insert_into_excel(row, column, data, sheet):
    # print(f'row {row} column {column} {data}')
    cell_value = sheet.cell(row=row, column=column).value or ' \n'
    sheet.cell(row=row, column=column).value = cell_value + data


def export_chromosome(chromosome, sheet):
    columns_and_rows = get_periods_as_rows_and_columns()
    start_row = 2
    start_column = 1
    period_nos = list(columns_and_rows)
    # insert headers as period
    for position, period in enumerate(period_nos):
        data = 'PERIOD ' + str(period_nos.index(period) + 1)
        insert_into_excel(start_row + position, start_column, data, sheet)

    start_row = 1
    start_column = 2
    period_dates = list(set([day for _, day in columns_and_rows]))
    period_dates = sorted(period_dates)
    # insert headers as days
    for position, day in enumerate(period_dates):
        data = 'DAY ' + str(period_dates.index(day) + 1)
        insert_into_excel(start_row, start_column + position, data, sheet)

    # insert row data
    for gene in chromosome['data']:
        period_id = gene['period_id']
        rooms = ', '.join([room['name'] for room in gene['rooms']])
        # get column isheetndex for period
        date = next((day for _period, day in columns_and_rows if int(_period) == int(period_id)))
        column_index = start_column + period_dates.index(date)
        row_index = start_row + period_id
        examCode = get_exam_name_from_id(gene['exam_id'])
        # print('Row index: ', row_index, '\nColumn index: ', column_index, '\nPeriod id: ', period_id, '\nDay Index: ', period_dates.index(date), '\nExam: ', examCode, '\nDay: ', date)
        data = f'{examCode}, {rooms}; '
        insert_into_excel(row_index, column_index, data, sheet)
    # print('days', period_dates)

def archive_logger(chromosomes):
    time_stamp = datetime.datetime.now()

    file_path = path.join(path.dirname(path.abspath(__file__)), f'../../data/archives/{time_stamp}.xlsx')
    excel_data_export(chromosomes, file_path)

def excel_data_export(chromosomes, file_path):
    # open workbook
    book = Workbook()
    sheet = book.active
    sheet.cell(row=1, column=2).value = "HARD CONSTRAINT VALUE"
    sheet.cell(row=1, column=3).value = "PENALTY VALUE"
    start_row = 2
    start_column = 1

    for position, chromosome in enumerate(chromosomes):
        data = "Chromosome " + str(chromosomes.index(chromosome) + 1)
        insert_into_excel(start_row + position, start_column, data, sheet)
    start_row = 1
    start_column = 2

    for position, chromosome in enumerate(chromosomes):
        data = chromosome['hard_constraint']
        sheet.cell(row=start_row + position + 1, column=start_column).value = data
        data = chromosome['soft_constraint']
        sheet.cell(row=start_row + position + 1, column=start_column + 1).value = data
    #     insert_into_excel(start_row + position, start_column + 1, data, sheet)
    for chromosome in chromosomes:
        name = "Chromosome " + str(chromosomes.index(chromosome) + 1)
        book.create_sheet(name)
        sheet2 = book[name]
        export_chromosome(chromosome, sheet2)

    # save workbook
    
    book.save(file_path)


if __name__ == "__main__":
    from main import app
    with app.app_context():
        population_size = int(input('Population Size: \t'))
        population = generate_population(population_size)
        with open('population.json', 'w') as f:
            json.dump(population, f, indent=1)
        # print(population[0][2]['rooms'][0]['name'])

    # pprint.pprint(population[0][1]['rooms'][0]['no_of_stds'])
        # population[0][0]['rooms'][0]['no_of_stds'] = 2000
        #  = 2000
        # population[0][2]['rooms'][0]['no_of_stds'] = 2000
        # population[0][0]['std_with_seats'] -= 1
        # population[0][1]['std_with_seats'] -= 1

        # closed_periods = get_closed_period()
        with open('population.json') as f:
            data = json.load(f)
        reserved_periods = read_period_preference()
        previous_chromosome = data[0]
        reserved_rooms = read_room_preference()

        closed_periods = [
        ]

        params = {
            'threshold': 1000,
            'closed_periods': closed_periods,
            'reserved_rooms': reserved_rooms,
            'reserved_periods': reserved_periods,
            'previous_chromosome': previous_chromosome,
            'prefered_rooms': [],  # get prefered rooms,r
            'prefered_periods':  []
        }
        updated_population = get_fitness_value(population, params)
        # pprint.pprint(updated_population[0]['soft_constraint'])
        file_path = path.join(path.dirname(path.abspath(__file__)), '../../data/Chromosome_data.xlsx')
        excel_data_export(updated_population, file_path)
        archive_logger(updated_population)
        # with open('updated_population.json', 'w') as f:
        #     json.dump(updated_population, f, indent=1)
        # pprint.pprint(non_dorminating_sort(updated_population))
        # for i in range(len(population[0])):
        #     pprint.pprint(population[0][i]['period_id'])
        # dorminating_chromosomes, non_dorminating_chromosomes = non_dorminating_sort(updated_population)
        # pprint.pprint(over_crowding(non_dorminating_chromosomes, dorminating_chromosomes))
        # updated_population = [ for chromosome in population]
        # fo pprint.pprint(chromosome)r chromosome in population:
        #     std_gene = get_specific_genes(1, chromosome)
        #     room_data = [gene['rooms'] for gene in chromosome]
        #     # room_names = [roo['no_of_stds'] for roo in room_data]
        #     pprint.pprint(room_data)
        # pprint.pprint(get_specific_genes(2, chromosome))
    # size = [len(chromosome) for chromosome in generated_chromosome]
    # print(size)

        # pprint.pprint(population[1][1]['period_id'])

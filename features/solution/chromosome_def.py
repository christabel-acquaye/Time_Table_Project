

import datetime
import openpyxl
from os import path
import pandas as pd
from features.periods.services import get_period_bound
from features.exam.services import get_exam_bound, get_exam_id_from_name
from features.solution.services import rand_gen
from features.solution.rooomAssign import period_room_allocation, room_compute
from features.solution.examAssign import period_exam_allocation
from features.exam.services import get_exam, get_exam_column, get_exam_order_by_size
from features.periods.services import get_period, get_periods_with_lengths, get_period_date
from features.rooms.services import get_rooms
from features.students.services import read_student_groups, get_exam_student_group, get_student_group_exams
import random
import json
import pprint
from sklearn.utils import shuffle
from errors import NotEnoughRooms


def format_rooms(rooms):
    return [{'name': room[1], 'no_of_stds': room[2]} for room in rooms]


def best_fit_exams_in_period(exams, duration):
    best_fit_exams = []  # exams less than duration
    new_exams_state = []  # exams which do not fit

    for exam in exams:
        if exam[1] <= duration:
            best_fit_exams.append(exam)
        else:
            new_exams_state.append(exam)

    return best_fit_exams, new_exams_state


def fit_exams_in_rooms(exams, rooms_available, period_id):
    """Fits exams in rooms and returns the exams catered for
    and the pending ones.
    Not all exams can be fitted withing the period since we can run
    out of rooms available when fitting the exams

    Arguments:
        exams {list} -- list of exams to attempt fitting
        rooms {[type]} -- [description]
        period_id {[type]} -- [description]
    """

    period_exams = []
    exams_without_rooms = []
    for position, exam in enumerate(exams):
        try:
            room_allocated, available_rooms = room_compute(
                exam[3],
                rooms_available[period_id - 1]
            )

            rooms_available[period_id - 1] = available_rooms
            # print('\trooms allocated', format_rooms(room_allocated))
            # print('\tstudents with seats', sum([ room[1] for room in format_rooms(room_allocated)]) )
            std_with_seats = sum(
                [room['no_of_stds']for room in format_rooms(room_allocated)]
            )

            if not std_with_seats == exam[3]:
                print('period', period_id, 'exam',
                      exam[0], 'std_size', exam[3])
                print("\tsome students didn't get seats, std_with_seats: %s, std_size: %s " % (
                    std_with_seats, exam[3]))  # problem was over here u forgot the % sign

            period_exam_assignment = {
                'period_id': period_id,
                'exam_id': exam[0],
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
    exams = get_exam_order_by_size()
    periods = get_periods_with_lengths()

    rooms = get_rooms()
    period_rooms = period_room_allocation(periods, rooms)

    # shuffle periods to add randomization
    periods = shuffle(periods, random_state=0)

    chromosome = []

    for period_id, period_duration in periods:
        # get exams with length < length of current period

        best_fit_exams, next_exams_period = best_fit_exams_in_period(
            exams,
            period_duration
        )

        period_exams, exams_without_rooms, period_rooms = fit_exams_in_rooms(
            best_fit_exams, period_rooms, period_id
        )

        # prepend unassigned exams to maintain exam order by size
        exams_without_rooms.extend(next_exams_period)
        exams = exams_without_rooms

        chromosome.extend(period_exams)
    
    return chromosome


def generate_population(size):
    return  [generate_chromosome()
                            for i in range(population_size)]

def a(chromosome):
    data = [gene['period_id'] for gene in chromosome]
    dates = [get_period_date(period) for period in data]
    return checkIfDuplicates_1(dates)

def checkIfDuplicates_1(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def get_specific_genes(std_id, chromosome):
    exams = get_student_group_exams(std_id)
    exams_id = [get_exam_id_from_name(examName=exam) for exam in exams[0]]
    genes = []
    for id in exams_id:
        res = [gene for gene in chromosome if gene["exam_id"] == id]
        genes.append(res)
    return genes
    


if __name__ == "__main__":
    population_size = int(input('Population Size: \t'))
    population = generate_population(population_size)
    # pprint.pprint(population)

    for chromosome in population:
        pprint.pprint(a(chromosome))
    # size = [len(chromosome) for chromosome in generated_chromosome]
    # print(size)

   
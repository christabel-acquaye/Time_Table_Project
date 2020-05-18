

import datetime
import json
import pprint
import random
from os import path

import openpyxl
import pandas as pd
from sklearn.utils import shuffle

from _shared import NotEnoughRooms
from features.exam.service import (get_exam_bound, get_exam_column,
                                   get_exam_id_from_name,
                                   get_exam_order_by_size, get_exams)
from features.periods.service import (get_period_bound, get_periods,
                                      get_periods_with_lengths)
from features.rooms.service import get_rooms
from features.solution.examAssign import period_exam_allocation
from features.solution.roomAssign import period_room_allocation, room_compute
from features.solution.services import rand_gen
from features.students.service import (get_exam_student_group,
                                       get_student_group_exams,
                                       read_student_groups)


def format_rooms(rooms):
    return [{'name': room['roomName'], 'no_of_stds': room['size']} for room in rooms]


def best_fit_exams_in_period(exams, duration):
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
                exam['minSize'],
                rooms_available[period_id - 1]
            )

            rooms_available[period_id - 1] = available_rooms
            # print('\trooms allocated', format_rooms(room_allocated))
            # print('\tstudents with seats', sum([ room[1] for room in format_rooms(room_allocated)]) )
            std_with_seats = sum(
                [room['no_of_stds']for room in format_rooms(room_allocated)]
            )

            if not std_with_seats == exam['minSize']:
                print('period', period_id, 'exam',
                      exam['id'], 'std_size', exam['minSize'])
                print("\tsome students didn't get seats, std_with_seats: %s, std_size: %s " % (
                    std_with_seats, exam['minSize']))  # problem was over here u forgot the % sign

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
    return [generate_chromosome()
            for i in range(population_size)]


def get_exam_from_gene(chromosome):
    return [gene["exam_id"] for gene in chromosome]


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
    from main import app
    with app.app_context():
        population_size = int(input('Population Size: \t'))
        population = generate_population(population_size)

        for chromosome in population:
            std_gene = get_specific_genes(1, chromosome)
            room_data = [gene['rooms'] for gene in chromosome]
            # room_names = [roo['no_of_stds'] for roo in room_data]
            pprint.pprint(room_data)
            # pprint.pprint(get_specific_genes(2, chromosome))
    # size = [len(chromosome) for chromosome in generated_chromosome]
    # print(size)



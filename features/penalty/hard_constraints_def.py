import datetime

import numpy as np

from features.periods.service import get_period_date
from features.solution.chromosome_def import (checkIfDuplicates_1,
                                              get_specific_genes)


def max_room_penalty(chromosome: List[dict]) -> int:
    """compute max rooms hard constraint
        0 - not to be assigned to a room
        1 - to be assigned one room
        2 - to be assigned two rooms
        3 - to be assigned three rooms
        4 - to be assigned four rooms

    Arguments:
        chromosome {List[dict]} -- chromosome

    Returns:
        int -- penalty value
    """
    pass


def more_than_one_exams_per_day(chromosome, student_group):
    data = [gene['period_id'] for gene in chromosome]
    dates = [get_period_date(period) for period in data]
    print(dates)
    if checkIfDuplicates_1(dates):
        return 2
    else:
        return 0


def back_to_back_conflict(chromosome, student_group):
    data = [gene['period_id'] for gene in chromosome]
    dates = [get_period_date(period) for period in data]
    dates.sort()
    count = 0
    for i in range(len(dates) - 1):
        if (dates[i+1] - dates[i]) == 1:
            count += 1
    return 4 * count


def get_room_distance(roomA, roomB):

    return split_distance


def distance_back_to_back_conflict(chromosome, student_group):
    split_distance = get_room_distance(roomA, roomB)
    if split_distance < 0 and split_distance > 1:
        return 2
    if split_distance < 1.1 and split_distance > 2:
        return 4
    if split_distance < 2.1 and split_distance > 5:
        return 7


def student_conflict(chromosome, student_group):
    std_conflict = []
    for student in student_group:
        std_conflict.append(more_than_one_exams_per_day(chromosome, student))
        std_conflict.append(back_to_back_conflict(chromosome, student))
        std_conflict.append(distance_back_to_back_conflict(chromosome, student))
    return std_conflict


def period_conflict(chromosome, period):
    return 5


def room_conflict(chromosome, room):
    return 5


def get_exam_room_assigned(exam):
    no_of_room = 0
    return no_of_room


def exam_conflict(chromosome, exam):
    exam_room_assigned = get_exam_room_assigned(exam)

    if exam_room_assigned == 0:
        return 0
    if exam_room_assigned == 1:
        return 1
    if exam_room_assigned == 2:
        return 2
    if exam_room_assigned == 3:
        return 3
    if exam_room_assigned == 4:
        return 4


def hard_constraints_value(chromosome, student_group, period, exam, room):
    hard_constraints = []

    hard_constraints.append(student_conflict(chromosome, student_group))
    hard_constraints.append(period_conflict(chromosome, period))
    hard_constraints.append(exam_conflict(chromosome, exam))
    hard_constraints.append(room_conflict(chromosome, room))

    return hard_constraints


if __name__ == "__main__":
    chromosome = []
    student_group = []
    period = []
    exam = []
    room = []
    val = hard_constraints_value(chromosome, student_group, period, exam, room)
    print(val)

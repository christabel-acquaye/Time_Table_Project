import datetime
import pprint

import numpy as np

from features.exam.service.__init__ import get_exam_room
from features.miscellaneous_functions import get_date_difference
from features.periods.service import get_period_date
from features.rooms.distance_services import get_distance_between_rooms
from features.students.service import get_all_student_ids, get_specific_genes


def more_than_one_exams_per_day(student_group_chromosome):
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    # pprint.pprint(dates[1])
    if checkIfDuplicates_1(dates):
        return 2
    else:
        return 0


def checkIfDuplicates_1(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


def back_to_back_conflict(student_group_chromosome):
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    dates.sort()
    count = 0
    print(dates)
    for i in range(len(dates) - 1):
        if (get_date_difference(dates[i+1], dates[i])) == 1:
            count += 1
    return 4 * count


def distance_back_to_back_conflict(student_group_chromosome):
<<<<<<< HEAD

    room_data = [gene['rooms'] for gene in std_gene]
    room_names = [room['no_of_stds'] for room in room_data]
    roomA, roomB = ''
    distance_back_to_back_conflict = []
    for i in range(len(room_names)):
        roomA = room_names[i]
        roomB = room_names[i+1]
        distnce = get_distance_between_rooms(roomA, roomB)
        actual_distance = distnce[0]

        if 0.1 <= actual_distance <= 1.0:
            distance_back_to_back_conflict.append(2)
        elif 1.1 <= actual_distance <= 2.0:
            distance_back_to_back_conflict.append(4)
        elif 2.1 <= actual_distance <= 5.0:
            distance_back_to_back_conflict.append(7)
        else:
            distance_back_to_back_conflict.append(0)
    return sum(distance_back_to_back_conflict)
=======
    # room_data = [gene['rooms'] for gene in student_group_chromosome]
    # room_names = []
    # for elem in room_data:
    #     room_name = [room['name'] for room in elem]
    #     print(room_name)
    #     room_names.append(room_name)
    # print(room_name[1])

    # if 0.1 <= actual_distance <= 1.0:
    #     distance_back_to_back_conflict.append(2)
    # elif 1.1 <= actual_distance <= 2.0:
    #     distance_back_to_back_conflict.append(4)
    # elif 2.1 <= actual_distance <= 5.0:
    #     distance_back_to_back_conflict.append(7)
    # else:
    #     distance_back_to_back_conflict.append(0)
    return 2
>>>>>>> 4910f23c6c8825742687dabaa1e4dd9167a34d7b


def student_conflict(chromosome, student_groups):
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    std_conflict = []
    for student_group_chromosome in std_gene:
        std_conflict.append(more_than_one_exams_per_day(student_group_chromosome))
        std_conflict.append(back_to_back_conflict(student_group_chromosome))
        std_conflict.append(distance_back_to_back_conflict(student_group_chromosome))
    return sum(std_conflict)


def period_conflict(chromosome):
    return 5


def room_conflict(chromosome):
    return 5


def exam_conflict(student_group_chromosome):
    exam_data = [gene['exam_id'] for gene in student_group_chromosome]
    exam_room_assigned = [get_exam_room(id) for id in exam_data]
    exam_conflicts = []
    for room_num in exam_room_assigned:
        if room_num == 0:
            exam_conflicts.append(0)

        if room_num == 1:
            exam_conflicts.append(1)

        if room_num == 2:
            exam_conflicts.append(2)

        if room_num == 3:
            exam_conflicts.append(3)

        if room_num == 4:
            exam_conflicts.append(4)
    return sum(exam_conflicts)


def get_total_hard_constraints_value(chromosome):
    hard_constraints = []
    # todo: call methods to return the data for these variables
    student_groups = get_all_student_ids()
    periods = []
    rooms = []
    hard_constraints.append(student_conflict(chromosome, student_groups))
    hard_constraints.append(period_conflict(chromosome))
    hard_constraints.append(exam_conflict(chromosome))
    hard_constraints.append(room_conflict(chromosome))

    return sum(hard_constraints)


if __name__ == "__main__":
    chromosome = []
    # student_group = []
    # period = []
    # exam = []
    # room = []
    # val = hard_constraints_value(chromosome, student_group, period, exam, room)
    # print(val)
    # roomA = 'OLD'
    # roomB = 'EHC 293'
    # print(get_room_distance_penalty(roomA, roomB))
    # distance_back_to_back_conflict(chromosome, 1)

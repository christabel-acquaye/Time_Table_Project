import datetime
import pprint
import math
import numpy as np

from features.exam.service.__init__ import get_exam_room
from features.miscellaneous_functions import get_date_difference
from features.periods.service import get_period_date
from features.rooms.distance_services import get_distance_between_rooms, find_average_distance
from features.students.service import get_all_student_ids, get_specific_genes


def more_than_one_exams_per_day(student_group_chromosome):
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    # pprint.pprint(dates[1])
    if has_duplicates(dates):
        return 2

    return 0


def has_duplicates(listOfElems):
    return len(listOfElems) != len(set(listOfElems))


def back_to_back_conflict(student_group_chromosome):
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    dates.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    count = 0
    for i in range(len(dates) - 1):
        if (get_date_difference(dates[i+1], dates[i])) == 1:
            count += 1
    return 4 * count


def distance_back_to_back_conflict(student_group_chromosome):
    hard_count = []
    for i in range(len(student_group_chromosome)):
        room_names1, room_names2 = [], []
        room_data1 = student_group_chromosome[i-1]['rooms']
        room_data2 = student_group_chromosome[i]['rooms']

        for elem in room_data1:
            room_name1 = [room['name'] for room in elem]
            room_names1.append(room_name1)
            if len(room_names1) < 1: continue
        
        for elem in room_data2:
            room_name2 = [room['name'] for room in elem]
            room_names2.append(room_name2)

        distance1 = find_average_distance(room_names1)
        distance2 = find_average_distance(room_names2)
        actual_distance = distance1 - distance2
        actual_distance = abs(actual_distance)

        if 0.1 <= actual_distance <= 1.0:
            distance_back_to_back_conflict.append(2)
        elif 1.1 <= actual_distance <= 2.0:
            distance_back_to_back_conflict.append(4)
        elif 2.1 <= actual_distance <= 5.0:
            distance_back_to_back_conflict.append(7)
        else:
            distance_back_to_back_conflict.append(0)
    return sum(hard_count)


def student_conflict(chromosome, student_groups):
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    std_conflict = []
    for student_group_chromosome in std_gene:
        std_conflict.append(more_than_one_exams_per_day(student_group_chromosome))
        std_conflict.append(back_to_back_conflict(student_group_chromosome))
        std_conflict.append(distance_back_to_back_conflict(student_group_chromosome))
    return len(std_conflict)


def period_conflict(chromosome, closed_periods, student_groups):
    hard_count = 0
    for gene in chromosome:
        current_period = gene['period_id']
        closed_exams = closed_periods.get(current_period, [])

        if not len(closed_exams):
            continue

        if not gene['exam_id'] in closed_exams:
            hard_count += 1

    # two exams for a student group should not have the same period
    for student_group_id in student_groups:
        std_exams = get_specific_genes(student_group_id, chromosome)
        std_exam_ids = list((gene['period_id'] for gene in std_exams))  # get period ids for student exams

        if has_duplicates(std_exam_ids):
            hard_count += 1

    # two exams or more in a day for different periods
        data = [gene['period_id'] for gene in std_exams]
        dates = [get_period_date(period) for period in data]
        ls = []
        for i in range(len(data)):
            item = {
                'period_id': data[i],
                'date': dates[i]
            }
        ls.sort(key=lambda item: datetime.datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S"))

    grouped = {}
    for ass in range(len(ls)):
        period_ls = []
        if ls[ass-1]['date'] == ls[ass]['date']:
            period_ls.append(ls[ass-1]['period'])
            period_ls.append(ls[ass]['period'])
        else:
            period_ls.append(ls[ass]['period'])
        grouped.update({
            ls[ass]['date']: period_ls
        })

    for key in grouped:
        if len(grouped[key]) > 1:
            if checkConsecutive(grouped[key]):
                print(key, '->', grouped[key])
                hard_count += 1

    return hard_count


def checkConsecutive(ls):
    return sorted(ls) == list(range(min(ls), max(ls)+1))


def room_conflict(chromosome, reserved_rooms):
    hard_count = 0
    std_exams = get_specific_genes(student_group_id, chromosome)
    data = [gene['rooms'] for gene in std_exams]
    for item in data:
        if item[name] in reserved_rooms:
            hard_count += 1
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
    return len(exam_conflicts)


def get_total_hard_constraints_value(chromosome, closed_periods, reserved_rooms):
    hard_constraints = []
    # todo: call methods to return the data for these variables
    student_groups = get_all_student_ids()
    periods = []
    rooms = []
    hard_constraints.append(student_conflict(chromosome, student_groups))
    hard_constraints.append(period_conflict(chromosome, closed_periods, student_groups))
    hard_constraints.append(exam_conflict(chromosome))
    hard_constraints.append(room_conflict(chromosome, reserved_rooms))

    return len(hard_constraints)


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

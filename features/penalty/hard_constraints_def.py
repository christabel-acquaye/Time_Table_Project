import numpy as np
from features.solution.chromosome_def import get_specific_genes, checkIfDuplicates_1
from features.periods.service import get_period_date
from features.rooms.distance_services import get_distance_between_rooms
from features.exam.service.__init__ import  get_exam_room
import datetime


def more_than_one_exams_per_day(chromosome, student_group):
    data = [gene['period_id'] for gene in chromosome]
    dates = [get_period_date(period) for period in data]
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
            count +=1
    return 4 * count


def distance_back_to_back_conflict(chromosome, student_group):
    std_gene = get_specific_genes(student_group, chromosome)
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

def student_conflict(chromosome, student_group):
    std_conflict = []
    for student in student_group:
        std_conflict.append(more_than_one_exams_per_day(chromosome, student))
        std_conflict.append(back_to_back_conflict(chromosome, student))
        std_conflict.append(distance_back_to_back_conflict(chromosome, student))
    return sum(std_conflict)

def period_conflict(chromosome, period):
    return 5
    

def room_conflict(chromosome, room):
    return 5

def exam_conflict(chromosome, student_group):
    std_gene = get_specific_genes(student_group, chromosome)
    exam_data = [gene['exam_id'] for gene in std_gene]
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


def hard_constraints_value(chromosome,
 student_group, period, exam, room):
    hard_constraints = []
   
    hard_constraints.append(student_conflict(chromosome, student_group))
    hard_constraints.append(period_conflict(chromosome, period))
    hard_constraints.append(exam_conflict(chromosome, exam))
    hard_constraints.append(room_conflict(chromosome, room))
   
    return hard_constraints


if __name__ == "__main__":
    chromosome =  []
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
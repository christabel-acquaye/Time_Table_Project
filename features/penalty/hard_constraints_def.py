import numpy as np

def more_than_one_exams_per_day(chromosome, student_group):
    return 2


def back_to_back_conflict(chromosome, student_group):
    return 4


def get_room_distance(roomA, roomB):

    return split_distance

def distance_back_to_back_conflict(chromosome, student_group):
    split_distance = get_room_distance(roomA, roomB)
    if split_distance < 0 and split_distance > 1 :
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
    chromosome =  []
    student_group = []
    period = []
    exam = []
    room = []
    val = hard_constraints_value(chromosome, student_group, period, exam, room)
    print(val)
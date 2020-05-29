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
    """Functions that checks to see if a student group has been assigned more than one exams in a day. 
        It gets all the period_id's in the chromosome and from that it gets the date for each chromosome.
        If the date returned is the same, it means we have at least two exams being written on the same day
    
    Arguments:
        student_group_chromosome {List[dict]} -- Contains exams written by only a particular student gorup

    Returns:
        int -- of 1 if there are periods with the same date and 0 if there exists no such condition/
    """
    hard_count = 0
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    # pprint.pprint(dates[1])
    if has_duplicates(dates):
        hard_count = 1

    return 2 * hard_count


def has_duplicates(listOfElems):
    return len(listOfElems) != len(set(listOfElems))


def back_to_back_conflict(student_group_chromosome):
     """Functions that checks to see if a student group has been assigned xams that directly follow another exams the next day
        It gets all the period_id's in the chromosome and from that it gets the date for each chromosome.
        It sorts the list in ascending order of dates
        If the difference between the previous date and the current date is 1, it means the student group has two exams on two conservative
        days during the exam period
    
    Arguments:
        student_group_chromosome {List[dict]} -- Contains exams written by only a particular student gorup

    Returns:
        int -- of 1 if there are periods with the same date and 0 if there exists no such condition
    """
    data = [gene['period_id'] for gene in student_group_chromosome]
    dates = [get_period_date(period) for period in data]
    dates.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    hard_count = 0
    for i in range(len(dates) - 1):
        if (get_date_difference(dates[i+1], dates[i])) == 1:
            hard_count += 1
    return 4 * hard_count


def distance_back_to_back_conflict(student_group_chromosome):
     """Distance back to back refers to the room distance between two adjacent papers by a student group on the same day;
        So you have period 1 and 2 on the same day and we realize, the student group has exams on these two periods,
        we calculate the distance between the rooms and it determines the penalty we assign for the distance back to back.
        NB: For the comparison of 2 rooms against 3 rooms, find the average distance between the 2 rooms and average distance
        between the 3 rooms and compare both average values.
    
    Arguments:
        student_group_chromosome {List[dict]} -- Contains exams written by only a particular student gorup

    Returns:
        int -- total distance back to back conflicts
    """
    
    hard_count = []
    for i in range(len(student_group_chromosome)):
        room_names1, room_names2 = [], []
        room_data1 = student_group_chromosome[i-1]['rooms']
        room_data2 = student_group_chromosome[i]['rooms']

        for elem in room_data1:
            room_name1 = [room['name'] for room in elem]
            room_names1.append(room_name1)
        
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
     """compute total hard constraints count for every student conflict

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        student groups [List] -- list of all student group ids.


    Returns:
        int -- hard_count value for student conflict
    """
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    std_conflict = []
    for student_group_chromosome in std_gene:
        std_conflict.append(more_than_one_exams_per_day(student_group_chromosome))
        std_conflict.append(back_to_back_conflict(student_group_chromosome))
        std_conflict.append(distance_back_to_back_conflict(student_group_chromosome))
    return len(std_conflict)


def period_conflict(chromosome, closed_periods, student_groups):
    """compute total hard constraints associated with period assigned in a specific chromosome. 
       It first checks to ensure that all closed periods; ie periods reserved for specific courses have been assigned correctly, else it assigns a 
       a hard_count of 1.
       It also checks to be sure no student group should have two exams for the same period and 
       if the student group also has two or more exams on consercutive periods.

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        student groups [List] -- list of all student group ids.

    Returns:
        int -- hard_count value for period conflict
    """
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
    """compute total hard constraints associated with rooms assigned in a specific chromosome. 
       It simply checks to be sure no room marked as reserved was assigned in the chromosome.

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        reserved_rooms [List] -- list of rooms reserved by the user.

    Returns:
        int -- hard_count value for every gene that has reserved rooms 
    """
    hard_count = 0
    std_exams = get_specific_genes(student_group_id, chromosome)
    data = [gene['rooms'] for gene in std_exams]

    for item in data:
        if item[name] in reserved_rooms:
            hard_count += 1
    return hard_count


def __get_difference(lenA, lenB):
    return (lenA - lenB)


def exam_conflict(student_group_chromosome):
    """compute total hard constraints associated with exams. It gets the max_rooms specified by user and the number of rooms assigned for every geen
       if the rooms assigned exceeds that speicifed by the user by 1: a hard_count of 1 is assigned
       if the rooms assigned exceeds that speicifed by the user by 2: a hard_count of 2 is assigned
       if the rooms assigned exceeds that speicifed by the user by 3: a hard_count of 3 is assigned
       if the rooms assigned exceeds that speicifed by the user by 4 and greater: a hard_count of 4 is assigned

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group
    

    Returns:
        int -- hard_count value for every gene that has more rooms than that specified
    """

    exam_data = [gene['exam_id'] for gene in student_group_chromosome]
    room_data = [gene['rooms'] for gene in student_group_chromosome]
    exam_room_assigned = [get_exam_room(id) for id in exam_data]
    hard_count = 0

    for i in range(len(exam_room_assigned)):
        if __get_difference(exam_room_assigned[i], len(room_data[i])) <= 0:
            hard_count = hard_count

        elif __get_difference(exam_room_assigned[i], len(room_data[i])) == 1:
            hard_count += 1

        elif __get_difference(exam_room_assigned[i], len(room_data[i])) == 2:
            hard_count += 2
        
        elif __get_difference(exam_room_assigned[i], len(room_data[i])) == 3:
            hard_count += 3

        elif __get_difference(exam_room_assigned[i], len(room_data[i])) >= 4 :
            hard_count += 4
    
    return hard_count


def get_total_hard_constraints_value(chromosome, closed_periods, reserved_rooms):
    """compute total hard constraints  for each chromosome in the population

    Arguments:
        chromosome {List[dict]} -- [description]
        params {dict} -- parameters data of closed_periods, and reserved periods

    Returns:
        int -- total hard constraints counted in the chromosome
    """
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

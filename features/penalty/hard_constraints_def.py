import datetime
import math
import pprint

import numpy as np

from features.exam.service.__init__ import get_exam_max_room
from features.miscellaneous_functions import get_date_difference, has_same_date
from features.periods.service import get_period_date
from features.rooms.distance_services import (find_average_distance,
                                              get_distance_between_rooms)
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
    for i in range(len(dates)):
        if has_same_date(dates[i], dates[i-1]):
            hard_count += 1
    return 2 * hard_count


def has_duplicates(listOfElems):
    return len(listOfElems) != len(set(listOfElems))


def back_to_back_conflict(student_group_chromosome):
    """Functions that checks to see if a student group has been assigned exams that directly
     follow another exams the next day. It gets all the period_id's in the chromosome and from that
     it gets the date for each chromosome. It sorts the list in ascending order of dates.
     If the difference between the previous date and the current date is 1, it means the student
     group has two exams on two conservative days during the exam period

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
    """Distance back to back refers to the room distance between two adjacent papers by a student
     group on the same day; So you have period 1 and 2 on the same day and we realize, the student
     group has exams on these two periods, we calculate the distance between the rooms and it
     determines the penalty we assign for the distance back to back. NB: For the comparison of 2
     rooms against 3 rooms, find the average distance between the 2 rooms and average distance
     between the 3 rooms and compare both average values.

    Arguments:
        student_group_chromosome {List[dict]} -- Contains exams written by only a particular student gorup

    Returns:
        int -- total distance back to back conflicts
    """

    hard_count = 0
    for i in range(len(student_group_chromosome)):
        distance1, distance2, actual_distance, distancels = 0, 0, 0, []
        roomA = [item['name'] for item in student_group_chromosome[i]['rooms']]
        roomB = [item['name'] for item in student_group_chromosome[i-1]['rooms']]
        if len(roomA) > 1 and len(roomB) > 1:
            distance1 = find_average_distance(roomA)
            distance2 = find_average_distance(roomB)
            actual_distance = abs(distance1 - distance2)

        elif len(roomA) == 1 and len(roomB) > 1:
            for i in range(len(roomB)):
                distance = get_distance_between_rooms(roomA[0], roomB[i])
                distancels.append(distance[0])
            actual_distance = sum(distancels) / len(roomB)

        elif len(roomA) > 1 and len(roomB) == 1:
            for i in range(len(roomA)):
                distance = get_distance_between_rooms(roomB[0], roomA[i])
                distancels.append(distance[0])
            actual_distance = sum(distancels) / len(roomA)

        elif len(roomA) == 1 and len(roomB) == 1:
            actual_distance = get_distance_between_rooms(roomA[0], roomB[0])
            actual_distance = actual_distance[0]

            hard_count += 2
        elif 1.1 <= actual_distance <= 2.0:
            hard_count += 4
        elif 2.1 <= actual_distance <= 5.0:
            hard_count += 7
        else:
            hard_count += 0
    return hard_count


def student_conflict(chromosome, student_groups):
    """compute total hard constraints count for every student conflict

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        student groups [List] -- list of all student group ids.


    Returns:
        int -- hard_count value for student conflict
    """
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    hard_count = []
    for student_group_chromosome in std_gene:
        # hard_count.append(more_than_one_exams_per_day(student_group_chromosome))
        # hard_count.append(back_to_back_conflict(student_group_chromosome))
        hard_count.append(distance_back_to_back_conflict(student_group_chromosome))
    return sum(hard_count)


def period_conflict(chromosome, closed_periods, student_groups):
    """compute total hard constraints associated with period assigned in a specific chromosome. 
       It first checks to ensure that all closed periods; ie periods reserved for specific courses 
       have been assigned correctly, else it assigns a hard_count of 1.
       It also checks to be sure no student group should have two exams for the same period and 
       if the student group also has two or more exams on consercutive periods.

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        student groups [List] -- list of all student group ids.

    Returns:
        int -- hard_count value for period conflict.
    """
    hard_count = 0
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    for student_group_chromosome in std_gene:
        data = [gene for gene in student_group_chromosome]
        for i in range(len(data)):
            for j in range(len(closed_periods)):
                if data[i]['period_id'] == closed_periods[j]['period_id'] and data[i]['exam_id'] == closed_periods[j]['exam_id']:
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


def room_conflict(chromosome, reserved_rooms, student_groups):
    """compute total hard constraints associated with rooms assigned in a specific chromosome. 
       It simply checks to be sure no room marked as reserved was assigned in the chromosome.

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group.
        reserved_rooms [List] -- list of rooms reserved by the user.

    Returns:
        int -- hard_count value for every gene that has reserved rooms 
    """
    hard_count = 0
    std_gene = [get_specific_genes(student_group_id, chromosome) for student_group_id in student_groups]
    for student_group_chromosome in std_gene:
        data = [gene for gene in student_group_chromosome]
        for i in range(len(data)):
            for j in range(len(reserved_rooms)):
                if data[i]['period_id'] == reserved_rooms[j]['period_id']:
                    data_name = [det['name'] for det in data[i]['rooms']]
                    if any(item in data_name for item in reserved_rooms[j]['reserved_rooms']):
                        hard_count += 1

    return hard_count


def __get_difference(lenA, lenB):
    return (lenA - lenB)


def exam_conflict(student_group_chromosome):
    """compute total hard constraints associated with exams. It gets the max_rooms specified by
     user and the number of rooms assigned for every gene if the rooms assigned exceeds that
     speicifed by the user by 1: a hard_count of 1 is assigned if the rooms assigned exceeds that
     speicifed by the user by 2: a hard_count of 2 is assigned if the rooms assigned exceeds that
     speicifed by the user by 3: a hard_count of 3 is assigned if the rooms assigned exceeds that
     speicifed by the user by 4 and greater: a hard_count of 4 is assigned.

    Arguments:
        chromosome {List[dict]} -- Contains exams written by only a particular student group


    Returns:
        int -- hard_count value for every gene that has more rooms than that specified
    """

    exam_data = [gene['exam_id'] for gene in student_group_chromosome]
    room_data = [gene['rooms'] for gene in student_group_chromosome]
    exam_room_assigned = [get_exam_max_room(id) for id in exam_data]
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

        elif __get_difference(exam_room_assigned[i], len(room_data[i])) >= 4:
            hard_count += 4

    return hard_count


def get_perturbation_penalty(previous_chromosome, current_chromosome):
    """Find the distance in terms of periods between exams in the initial time table and those in the new one

    Arguments:
        previous_chromosome {List[dict]} -- Contains data for a previously generated penalty.
        current_chromosomes {List[dict]} -- Contains data for a chromosome in the generated population.

    Returns:
        int -- total penalty value based on distance diff. between the previously generated timetable
         and a specific chromosome in a pop. 
    """
    penalty = 0
    for i in range(len(previous_chromosome)):
        previous_chromosome_exam_id = previous_chromosome[i]['exam_id']
        key = 'exam_id'
        position_in_curr_chromosome = get_position_in_chromosome(current_chromosome, key, previous_chromosome_exam_id)
        penalty += (previous_chromosome[i]['period_id'] - current_chromosome[position_in_curr_chromosome]['period_id'])

    return penalty


def get_total_hard_constraints_value(chromosome, closed_periods, reserved_rooms, previous_chromosome):
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
    hard_constraints.append(room_conflict(chromosome, reserved_rooms, student_groups))
    # if previous_chromosome:
    #     hard_constraints.append(get_perturbation_penalty(previous_chromosome, chromosome))
    return sum(hard_constraints)


def get_position_in_chromosome(chromosome, key, value):
    for i, dic in enumerate(chromosome):
        if dic[key] == value:
            return i
    return -1


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

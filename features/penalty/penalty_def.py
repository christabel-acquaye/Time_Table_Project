import pprint
from typing import List

from features.exam.service.__init__ import (get_exam_enrollment,
                                            get_exam_max_room)
from features.periods.service.__init__ import get_period_penalty
from features.rooms.distance_services import (find_average_distance,
                                              get_distance_between_rooms)
from features.rooms.service.__init__ import get_room_penalty, get_room_size


def period_penalty(gene, reserved_periods):
    """if a period is opened, we assign weights
    -4: strongly prefered
    -1: prefered
    0: neutral
    1: discouraged
    4: strongly discouraged

    Arguments:
        gene {dict} -- gene
        reserved_periods [list] -- periods reserved for specific occasions

    Returns:
        int -- penalty value
    """

    penalty = 0

    # penalty = get_period_penalty(gene['period_id'])
    if gene['period_id'] in reserved_periods:
        penalty += 4
    data = [elem['no_of_stds'] for elem in gene['rooms']]
    enrollment = get_exam_enrollment(gene['exam_id'])
    if gene['std_with_seats'] < enrollment:
        penalty += 1

    return penalty


def room_availability_penalty(gene: dict):
    """Function that calculates penalties related to the room availability.
            It checks if room was over assigned.
            If specified max room matches total number of rooms.
            If rooms assigned for a particular assignment is in the same area.

        -4: strongly prefered
        -1: prefered
        0: neutral
        1: discouraged
        4: strongly discouraged

    Arguments:
        gene {dict} -- gene

    Returns:
        int -- penalty value
    """

    penalty = 0
    room_size = [get_room_size(item['name']) for item in gene['rooms']]
    ass_room_size = [item['no_of_stds'] for item in gene['rooms']]
    for i in range(len(room_size)):
        if ass_room_size[i] > room_size[i]:
            print(room_size[i], ass_room_size[i])
            penalty += 4

    if len(room_size) > get_exam_max_room(gene['exam_id']):
        penalty += 4

    rooms = [item['name'] for item in gene['rooms']]
    # print(len(rooms))
    if len(rooms) > 1:
        if (find_average_distance(rooms)) > 0:
            penalty += 4
        else:
            penalty = penalty
    return penalty


def chkList(lst):
    return len(set(lst)) == 1


def room_split_penalty(gene: dict):
    no_of_rooms = len(gene['rooms'])
    return compute_split_penalty(no_of_rooms)


def compute_split_penalty(no_of_rooms: int):
    """compute split penalty
    Arguments:
        no_of_rooms {int} -- number of rooms
    """
    return (no_of_rooms - 1) ** 2


def room_size_penalty(gene):
    """ Function that checks the the percentage of seats occupied of a particular exams.
      If the percetage falls within a specified range, a particular penalty is assigned.
          • 1 – 10% of capacity; penalty = 1
          • 10 – 30% of capacity; penalty = 0
          • 30 – 60% of capacity; penalty = -1
          • 60 – 100% of capacity; penalty = -2

    Argument:
        gene {dict} -- gene

    Returns:
        int -- Sum of the total penalty for each room assigned in the gene

    """

    rooms = gene['rooms']
    penalty = []
    used = [single_room['no_of_stds'] for single_room in rooms]
    actual = [get_room_size(single_room['name']) for single_room in rooms]
    for i in range(len(used)):
        percentage = (used[i] / actual[i]) * 100

        if 1 <= percentage <= 10:
            penalty.append(1)
        elif 10 <= percentage <= 30:
            penalty.append(0)
        elif 30 <= percentage <= 60:
            penalty.append(-1)
        else:
            penalty.append(-2)
    return sum(penalty)


def exam_enrolment_penalty(gene, threshold):
    """calaculates the penalty for the percentage the exam enrollment size exceeds a specific threshold
        • 1 – 10% more than threshold; penalty = 1
        • 10 – 30% more than threshold; penalty = 5
        • 30 – 60% more than threshold; penalty = 10
        • 60 – 100% more than threshold; penalty = 20
    Arguments:
        chromosome {List[dict]} -- [description]
        threshold int -- threshold

    Returns:
        int -- total penalty calculated for the gene
    """
    penalty = []
    enrolment = get_exam_enrollment(gene['exam_id'])
    percentage = ((enrolment - threshold) * 100)/threshold
    percentage_increase = percentage - 100

    if 1 <= percentage_increase <= 10:
        penalty.append(1)
    elif 10 <= percentage_increase <= 30:
        penalty.append(5)
    elif 30 <= percentage_increase <= 60:
        penalty.append(10)
    elif 60 <= percentage_increase <= 100:
        penalty.append(20)
    else:
        penalty.append(0)
    return sum(penalty)


def get_total_penalty_value(chromosome: List[dict], threshold: int, reserved_periods) -> int:
    """compute total penalty or chromosome

    Arguments:
        chromosome {List[dict]} -- [description]
        params {dict} -- parameters data

    Returns:
        int -- [description]
    """
    penalty = []

    for gene in chromosome:
        penalty.append(period_penalty(gene, reserved_periods))

        penalty.append(room_availability_penalty(gene))
        penalty.append(room_split_penalty(gene))
        penalty.append(room_size_penalty(gene))
        penalty.append(exam_enrolment_penalty(gene, threshold))

    return sum(penalty)

import pprint
from typing import List

from features.exam.service.__init__ import get_exam_enrollment
from features.periods.service.__init__ import get_period_penalty
from features.rooms.service.__init__ import get_room_penalty, get_room_size


def period_penalty(gene, reserved_periods):
    penalty = 0

    # penalty = get_period_penalty(gene['period_id'])
    if gene['period_id'] in reserved_periods:
        penalty += 4
    data = [elem['no_of_student'] for elem in gene['rooms']]
    enrollment = get_exam_enrollment(gene['exam'])
    if sum(data) < enrollment:
        penalty += 1

    """if a period is opeed, we assign weights
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
    return penalty


def room_availability_penalty(gene: dict):
    penalty = 0
    room_size = [get_room_size(item['name']) for item in gene['rooms']
    ass_room_size = [item['no_of_students'] for item in gene['rooms']
    for i in range(len(room_size)):
        if ass_room_size[i] > room_size[i]
            penalty += 4
    
    if len(room_size) != get_exam_enrollment(gene['exam']):
        penalty += 4
    """if a room is not available, we aenrollment = get_exam_enrollment(gene['exam'])ssign weights
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

    return penalty


def chkList(lst):
    return len(set(lst)) == 1


def check_exams_in_same_vicinity(gene):
    penalty = 0
    firsts = [item['name'] for item in gene['rooms']]
    if chkList(firsts) == False:
        penalty += 4


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
    else:
        penalty.append(20)
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

from typing import List
from features.rooms.service.__init__ import  get_room_size
from features.exam.service.__init__ import get_exam_enrollment
from features.periods.service.__init__ import get_period_penalty


def period_penalty(gene):
    
    """if a period is opened, we assign weights
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
    pass


def room_availability_penalty(gene: dict) -> int:
    """if a room is not available, we assign weights
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

    pass


def room_split_penalty(gene):
    room_data = [assignment['rooms'] for assignment in gene]
    room_size_penalty = []
    for room in room_data:
        no_of_rooms = len(room_data)
        if no_of_rooms == 1:
            room_split_penalty.append(0)
        if no_of_rooms == 2:
            room_split_penalty.append(1)
        if no_of_rooms == 3:
            room_split_penalty.append(4)
        if no_of_rooms == 4:
            room_split_penalty.append(7)
    return sum(room_split_penalty)


def compute_split_penalty(no_of_rooms: int):
    """compute split penalty

    Arguments:
        no_of_rooms {int} -- number of rooms
    """
    return (no_of_rooms - 1) ** 2


def room_size_penalty(gene):
    room_data = [assignment['rooms'] for assignment in gene]
    room_size_penalty = []
    
    for rooms in room_data:
        used = [single_room['no_of_size'] for single_room in rooms]
        actual =  [get_room_size(single_room['name'] for single_room in rooms)
        for i in range(0, len(used)):
            percentage = (used[i]/actual[i])*100
            if 1 <= actual_distance <= 10:
                room_size_penalty.append(1)
            if 10 <= actual_distance <= 30:
                room_size_penalty.append(0)
            if 30 <= actual_distance <= 60:
                room_size_penalty.append(-1)
            if 60 <= actual_distance <= 100:
                room_size_penalty.append(-2)
    
    return sum(room_split_penalty)


def exam_enrolment_penalty(gene, threshold):
    exam_enrolment_penalty = []
    exam_data = [assignment['exam_id'] for assignment in gene]
    for exam in exam_data:
        enrollment = get_exam_enrollment(exam)
        percentage = ((enrollment-threshold) * 100)/threshold
        percentage_increase =  percentage - 100
        if 1 <= percentage_increase <= 10:
            exam_enrolment_penalty.append(1)
        if 10 <= percentage_increase <= 30:
            exam_enrolment_penalty.append(5)
        if 30 <= percentage_increase <= 60:
            exam_enrolment_penalty.append(10)
        if 60 <= percentage_increase <= 100:
            exam_enrolment_penalty.append(20)
        
    return sum(exam_enrolment_penalty)


def get_total_penalty_value(chromosome: List[dict], params: dict) -> int:
    """compute total penalty or chromosome

    Arguments:
        chromosome {List[dict]} -- [description]
        params {dict} -- parameters data

    Returns:
        int -- [description]
    """
    penalty = []

    for gene in chromosome:
        penalty.append(period_penalty(gene))
        penalty.append(room_availability_penalty(gene))
        penalty.append(max_room_penalty(gene))
        penalty.append(room_split_penalty(gene))
        penalty.append(room_size_penalty(gene))
        penalty.append(exam_enrolment_penalty(gene, params['threshold']))

    return sum(penalty)

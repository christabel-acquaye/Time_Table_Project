from typing import List


def period_penalty(gene: dict) -> int:
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


def room_split_penalty(gene: dict) -> int:
    """if exam is split to several rooms return penalty value

    Arguments:
        gene {dict} -- [description]

    Returns:
        int -- [description]
    """
    pass


def compute_split_penalty(no_of_rooms: int):
    """compute split penalty

    Arguments:
        no_of_rooms {int} -- number of rooms
    """
    return (no_of_rooms - 1) ** 2


def room_size_penalty(gene: dict) -> int:
    """determine the room size range
    1 - 10% - penalty 1
    10 - 30% - penalty 0
    30 - 60% - penalty -1
    60 - 100% - penalty -2

    Arguments:
        gene {dict} -- [description]

    Returns:
        int -- [description]
    """
    pass


def exam_enrolment_penalty(gene: dict, threshold: int) -> int:
    """exam with enrolment greater than threshold
    1 - 10% - penalty 1
    10 - 30% - penalty 5
    30 - 60% - penalty 10
    60 - 100% - penalty 20


    Arguments:
        gene {dict} -- [description]
        threshold {int} -- [description]

    Returns:
        int -- [description]
    """
    pass


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

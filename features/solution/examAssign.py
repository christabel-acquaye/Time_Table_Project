import pprint
import random

from features.exam.service import get_exam_bound, get_exam_order_by_size
from features.periods.service import get_periods
from features.solution.services import rand_gen


# Function that generates a random period and assigns it to an exam.
def period_exam_allocation(exams):
    period_finsih = get_period_bound() + 1
    ran_period = 0
    period_exams = []
    for exam in exams:
        ran_period = random.randint(1, period_finsih)
        period_exam_assignment = {
            'Period id': ran_period,
            'Exam id': exam[0]
        }
        period_exams.append(period_exam_assignment)
    return period_exams


if __name__ == "__main__":
    data = period_exam_allocation(get_exam())
    pprint.pprint(data)

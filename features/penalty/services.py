
from features.students.services import read_student_groups
from features.exam.services import get_exam
import pprint


def get_exam_student_group(exam_name, std_group):
    return [exam[0] for exam in std_group if exam_name in std_group[1:]]


# # Function that gets genes for exams of particular student groups
# def get_std_group_exam_assignment(chromosome, exam):
#     return [gene for gene in chromosome if gene['exam_id'] = exam[0]]

# def get_period_date(period):
#     return period[2]
# def get_std_group_exam_assignment(chromosome, exam):
#     return [gene for ]

if __name__ == '__main__':

    # exams = get_exam()
    std_groups = read_student_groups()
    pprint.pprint(read_student_groups())
    # print(get_exam_student_group(exams, std_groups))

import random
import pprint
from features.migration import read_student
from features.exam.service import get_exams


# Function that generates a random array within a specified range
def rand_gen(start, finish):
    finish += 1
    rand_arr = list(range(start, finish))
    random.shuffle(rand_arr)
    return rand_arr


# Function that matches a particular exam id to a student group
def get_exam_student_group_match(exam, student_group):
    related_course = []

    for course in student_group:
        # pprint.pprint(course['course'])
        if exam in course['course']:
            related_course.append(course['id'])

    # pprint.pprint(related_course)
    return related_course


# Function that returns all students offering similar courses.
def get_exam_search():
    exam_student_group = []

    data = read_student()

    exams = get_exam()

    start = 1
    finish = get_exam_bound()

    rand_arr = rand_gen(start=start, finish=finish)
    for id in rand_arr:
        exam_id = id
        # print(exam_id)
        exam = get_exam(id=exam_id)
        examCode = get_exam_column(columnName='examCode', id=exam_id)
        # print(examCode[0][0])
        group = get_exam_student_group_match(exam=examCode[0][0], student_group=data)
        exam_student_group.append(group)
    return exam_student_group


def get_digit_multiplication_factor(max, min, maxDgt, gene_size):
    digit_multiplication_factor = (max - min) / (maxDgt * gene_size)
    return digit_multiplication_factor


if __name__ == "__main__":

    data = get_digit_multiplication_factor(120, 1, 9, 2)
    print(data)

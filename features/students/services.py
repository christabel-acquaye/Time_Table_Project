
import pprint
from os import path

import MySQLdb
import numpy as np
import pandas as pd
from MySQLdb._exceptions import Error

from features.exam.services import get_exam
from playground import connect

# Insert Data into Students Table


@connect
def insert_students(cur, id, examId, periodId):
    insert_query = """INSERT INTO student(id, examId, periodId)
                        VALUES (
                        "{id}","{examId}", "{periodId}" 
                      )
        """.format(
        periodId=periodId,
        examId=examId,
        id=id
    )

    try:
        cur.execute(insert_query)

        # print(cur.fetchall(), "Student Added Successfully...")

    except Error as e:
        print(e)


# Get all Students
@connect
def get_students(cur, id=None):
    data = []
    get_query = "SELECT * FROM student"
    if id:
        get_query += " WHERE id = {}".format(id)
    try:
        cur.execute(get_query)

        print(cur.fetchall(), "Displaying all results from Student Table...")
        data = cur.fetchall()

    except Error as e:
        print(e)

    return data


def read_student_groups():
    file_path = path.join(path.dirname(path.abspath(__file__)), '../../data')
    data = []
    raw_data = pd.read_csv(file_path + '/students.csv')
    for row in raw_data.to_dict('record'):
        data.append(
            tuple((value for value in row.values() if not pd.isna(value))))

    return data


def get_exam_student_group(exam_name, std_groups):
    return [exam[0] for exam in std_groups if exam_name in exam]


def get_student_group_exams(std_id):
    student_group = read_student_groups()
    exams = [student[1:] for student in student_group if student[0] == std_id]
    exam_list = [list(elem) for elem in exams]
    return exam_list


if __name__ == '__main__':

    # insert_students(id = '1', examId = '10', periodId = '23')
    std_groups = read_student_groups()
    pprint.pprint(get_student_group_exams(2))
    # print(get_exam_student_group('ENGL 352', std_groups))
    # pprint.pprint(get_student_group_exams(get_exam(), read_student_groups()))

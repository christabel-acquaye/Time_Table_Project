
import MySQLdb
from _mysql_exceptions import Error
import pandas as pd
from playground import connect
from os import path
import numpy as np


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


if __name__ == '__main__':

    # insert_students(id = '1', examId = '10', periodId = '23')
    std_groups = read_student_groups()
    print(get_exam_student_group('ENGL 352', std_groups))

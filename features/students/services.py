from uuid import uuid4

import MySQLdb
from _mysql_exceptions import Error

from playground import connect


# Insert Data into Students Table
@connect
def insert_students(cur, examId, periodId):
    insert_query = """INSERT INTO students(id, examId, periodId)
                        VALUES (
                        "{id}","{examId}", "{periodId}" 
                      )
        """.format(
        periodId=periodId,
        examId=examId,
        id=uuid4().__str__()
    )

    try:
        cur.execute(insert_query)

        print(cur.fetchall(), "Student Added Successfully...")

    except Error as e:
        print(e)


# Get all Students
@connect
def get_students(cur, id=None):
    get_query = "SELECT * FROM students"
    if id:
        get_query += " WHERE id = {}".format(id)
    try:
        cur.execute(get_query)

        print(cur.fetchall(), "Displaying all results from Student Table...")


    except Error as e:
        print(e)



if __name__ == '__main__':
    id = uuid4().__str__()

from uuid import uuid4

import MySQLdb
from _mysql_exceptions import Error

from playground import connect


# Insert Data into Assignments Table
@connect
def insert_assignment(cur, periodId, roomId, examId):
    insert_query = """INSERT INTO assignment(periodId, roomId, examId)
                        VALUES (
                        "{periodId}", "{roomId}","{examId}"  
                      )
        """.format(
        periodId=periodId,
        examId=examId,
        roomId=roomId
    )

    try:
        cur.execute(insert_query)

        print(cur.fetchall(), "Assignment Added Successfully...")

    except Error as e:
        print(e)


# Get all Assignments
@connect
def get_assignment(cur,id=None):
    get_query = "SELECT * FROM assignment"
    if id:
        get_query += 'WHERE id = "{}"'.format(id)

    try:
        cur.execute(get_query)

        print(cur.fetchall(), "Displaying all results from Assignment Table...")


    except Error as e:
        print(e)


if __name__ == '__main__':
    period_id = uuid4().__str__()
    room_id = uuid4().__str__()
    exam_id = uuid4().__str__()


    insert_assignment(periodId=period_id, roomId=room_id, examId=exam_id)

    # get_assignment()
    get_assignment()
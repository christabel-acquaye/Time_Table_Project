from uuid import uuid4

import MySQLdb
from MySQLdb._exceptions import Error

from playground import connect


# Insert exam room assignments into Exam Room Table
@connect
def insert_exams_rooms(cur, examId, roomId):
    insert_query = """INSERT INTO examRoomRelation(examId, roomId)
                        VALUES (
                        "{examId}", "{roomId}" 
                      )
        """.format(
        examId=examId,
        roomId=roomId,
    )

    try:

        cur.execute(insert_query)

        print(cur.fetchall(), "Item Added Successfully...")
    except Error as e:
        print(e)


# Get all Items
@connect
def get_exam_room(cur,id =None):
    get_query = "SELECT * FROM examRoomRelation"
    if id:
        get_query += " WHERE id = {}".format(id)
    try:
        cur.execute(get_query)

        print(cur.fetchall(), "Displaying results from Exam Room Relationship Table...")


    except Error as e:
        print(e)


if __name__ == '__main__':
    id = uuid4().__str__()

import MySQLdb
from _mysql_exceptions import Error

from playground import connect


# Insert Data into Students Table
@connect
def insert_students(cur,id, examId, periodId):
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

if __name__ == '__main__':
    

    # insert_students(id = '1', examId = '10', periodId = '23')
    arr = get_students()
    print(arr)
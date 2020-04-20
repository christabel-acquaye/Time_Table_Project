import MySQLdb
from uuid import uuid4

from _mysql_exceptions import Error

from playground import connect


# Insert Data into Exam Table
@connect
def insert_exam(cur, length, id, alt, minSize, maxRooms, average, examCode):
    insert_query = """INSERT INTO exams(id, length, alt, minSize, maxRooms, average, examCode )
                            VALUES (
                            "{id}",{length}, "{alt}" , {minSize}, {maxRooms}, "{average}", "{examCode}"
                          )
            """.format(
        length=length,
        alt=alt,
        id=id,
        minSize=minSize,
        maxRooms=maxRooms,
        examCode = examCode,
        average = average

    )

    # print(insert_query)
    cur.execute(insert_query)



# Get all Exam
@connect
def get_exam(cur, id=None):
    get_query = "SELECT * FROM exams "
    if id:
        get_query += ' WHERE examCode = "{}"'.format(id)

    try:
        cur.execute(get_query)

        print(cur.fetchall(), "Displaying  results from Exams Table...")


    except Error as e:
        print(e)


# Delete specific Exam details
@connect
def delete_exam(cur, id=None):
    delete_query = "DELETE FROM exams "
    if id:
        delete_query += ' WHERE examCode = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Exams Table...")


    except Error as e:
        print(e)

# Update specific Exam details
@connect
def delete_exam(cur, id=None):
    delete_query = "DELETE FROM exams "
    if id:
        delete_query += ' WHERE examCode = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Exams Table...")


    except Error as e:
        print(e)



if __name__ == '__main__':
    id = "2"
    length = 125
    alt = True
    minSize = 21
    maxRooms = 2
    average = 10
    examCode = "CAT 152"



    # insert_exam(id = id,length= length, alt = alt, minSize = minSize,maxRooms =  maxRooms, average = average, examCode = examCode)
    # get_exam()

    get_exam(id = examCode)

    # delete_exam(id=examCode)


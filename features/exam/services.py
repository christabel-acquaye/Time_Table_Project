import MySQLdb
from uuid import uuid4

from _mysql_exceptions import Error

from playground import connect


# Insert Exam details into Exam Table
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

    cur.execute(insert_query)



# Get exam 
@connect
def get_exam(cur, id=None):
    get_query = "SELECT * FROM exams "
    if id:
        get_query += ' WHERE id = "{}"'.format(id)

    try:
        data = cur.execute(get_query)
        data = cur.fetchall()

    except Error as e:
        print(e)
    return data


# Get Specific  Exam deatils for a particular exams column
@connect
def get_exam_column(cur, columnName, id=None):
    get_query = "SELECT "
    get_query += columnName 
    get_query += " FROM exams "
    data = []
    if id:
        get_query += ' WHERE id = '
        
        get_query += '"{}"'.format(id)

    try:
        data = cur.execute(get_query)
        data = cur.fetchall()
        return data

    except Error as e:
        print(e)

# Function that gets all exams arranged by decreasing order of enrollment size
@connect
def get_exam_order_by_size(cur):
    get_query = "SELECT * FROM exams ORDER BY minSize DESC"
   
    try:
        data = cur.execute(get_query)
        data = cur.fetchall()

    except Error as e:
        print(e)
    return data


# Get total number of exams in db
@connect
def get_exam_bound(cur):
    get_query = "Select count(*) from exams;"
 

    try:
        data = cur.execute(get_query)
        data = cur.fetchall()

    except Error as e:
        print(e)
    return int(data[0][0])



# Delete specific Exam details
@connect
def delete_exam(cur, id=None):
    delete_query = "DELETE FROM exams "
    if id:
        delete_query += ' WHERE examCode = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Exams Table...")
        get_exam(id = id)

    except Error as e:
        print(e)



# Update specific Exam details
@connect
def update_exam(cur, columnName, update, id=None):
    update_query = "UPDATE exams SET "
    update_query += columnName
    update_query += ' = "{}"'.format(update)
    if id:
        update_query += 'WHERE examCode = "{}"'.format(id)

    try:
        cur.execute(update_query)

        print(cur.fetchall(), "Updating hits from Exams Table...")


    except Error as e:
        print(e)



if __name__ == '__main__':
    id = "42"
    length = 125
    alt = True
    minSize = 21
    maxRooms = 2
    average = 10
    examCode = "IRAI ALL"
    columnName = 'length'
    update = 120

    # insert_exam(id = id,length= length, alt = alt, minSize = minSize,maxRooms =  maxRooms, average = average, examCode = examCode)
    # update_exam(columnName = columnName, update = update, id=examCode)
    # get_exam()
  
    # get_exam(id = id)

    # delete_exam(id=examCode)

    # get_exam_column(columnName='id', id=None)
    
    data =  get_exam_order_by_size()
    print(data)
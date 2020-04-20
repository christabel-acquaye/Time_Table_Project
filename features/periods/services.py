import MySQLdb
from _mysql_exceptions import Error
from playground import connect
from uuid import uuid4


# Insert Data into Period Table
@connect
def insert_period(cur, id,  length, day, time, penalty):
    # print(length, day, time, penalty)
    insert_query = """INSERT INTO periods(id, length, day, time, penalty)
                        VALUES (
                        "{id}",{length}, "{day}" , "{time}", {penalty}
                      )
        """.format(
        length=length,
        day=day,
        time=time,
        penalty=penalty,
        id=id
    )

    # print(insert_query)
    try:
        cur.execute(insert_query)

        print(cur.fetchall(), "Exam Period Added Successfully...")

    except Error as e:
        print(e)


# Get all Periods
@connect
def get_period(cur, penalty=None):
    get_query = "SELECT * FROM periods"
    if id:
        get_query += ' WHERE penalty = "{}"'.format(penalty)

    cur.execute(get_query)

    print(cur.fetchall(), "Displaying  results from Periods Table...")



# Delete specific Period details
@connect
def delete_period(cur, id=None):
    delete_query = "DELETE FROM periods "
    if id:
        delete_query += ' WHERE penalty = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Periods Table...")


    except Error as e:
        print(e)


if __name__ == '__main__':

    length = 120
    day = "1997-06-04"
    time = "8:00am-11:30am"
    penalty = 1
    id = "23"

    insert_period(
                  length=length,
                  day=day,
                  time=time,
                  penalty=penalty,
    id = id)
    # get_period(penalty = penalty)
import MySQLdb
from _mysql_exceptions import Error
from playground import connect
from uuid import uuid4


# Insert PEriod deatils into Period Table
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


    try:
        cur.execute(insert_query)

        print(cur.fetchall(), "Exam Period Added Successfully...")

    except Error as e:
        print(e)

# Get total number of periods in db
@connect
def get_period_bound(cur):
    get_query = "Select count(*) from periods;"
 

    try:
        data = cur.execute(get_query)
        data = cur.fetchall()

    except Error as e:
        print(e)
    return int(data[0][0])



# Get all Periods in db
@connect
def get_period(cur, penalty=None):
    get_query = "SELECT * FROM periods"
    if penalty:
        get_query += ' WHERE penalty = "{}"'.format(penalty)
    try:
        data = cur.execute(get_query)
        data = cur.fetchall()
    except Error as e:
        print(e)
    return data

# Get all Periods in db
@connect
def get_period_date(cur, id=None):
    get_query = "SELECT day FROM periods"
    if id:
        get_query += ' WHERE id = "{}"'.format(id)
    try:
        data = cur.execute(get_query)
        data = cur.fetchall()
    except Error as e:
        print(e)
    return data

# Delete specific Period details
@connect
def delete_period(cur, penalty=None):
    delete_query = "DELETE FROM periods "
    if penalty:
        delete_query += ' WHERE penalty = "{}"'.format(penalty)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Periods Table...")
        get_period(penalty=penalty)

    except Error as e:
        print(e)


# Update specific Period details
@connect
def update_period(cur, columnName, update, id=None):
    update_query = "UPDATE periods SET "
    update_query += columnName
    update_query += ' = "{}"'.format(update)
    if id:
        update_query += 'WHERE id = "{}"'.format(id)

    try:
        cur.execute(update_query)

        print(cur.fetchall(), "Updating hits from Periods Table...")


    except Error as e:
        print(e)


def get_periods_with_lengths():
    return list(((int(period[0]), period[1]) for period in get_period()))


if __name__ == '__main__':

    # length = 120
    # day = "1997-06-04"
    # time = "8:00am-11:30am"
    # penalty = 1
    # id = "3"
    # print(list(get_periods_with_lengths()))
    print(get_period_date(id = 1))

    # insert_period(
    #               length=length,
    #               day=day,
    #               time=time,
    #               penalty=penalty,
    # id = id)
    # get_period(penalty = penalty)
    # update_period(columnName = 'length', update = 100, id=id)
    # delete_period(penalty=penalty)
    # get_period()
    # data = get_period()
    # print(data)
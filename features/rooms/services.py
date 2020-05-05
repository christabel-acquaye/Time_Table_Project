import MySQLdb
from _mysql_exceptions import Error

from playground import connect
from uuid import uuid4
from MySQLdb import escape_string


# Insert Data into Rooms Table
@connect
def insert_rooms(cur, id, roomName, size, alt, coord_longitude, coord_latitude):
    insert_query = """INSERT INTO rooms(id, roomName, size, alt, Coord_Longitude, Coord_Latitude)
                        VALUES (
                        "{id}", "{roomName}", {size}, {alt} , "{coord_longitude}", "{coord_latitude}"
                      )
        """.format(
        size=size,
        alt=alt,
        id=id,
        roomName = roomName,
        coord_longitude = coord_longitude,
        coord_latitude = coord_latitude
    )

    cur.execute(insert_query)


@connect
def get_rooms(cur, id=None):

    # Get all Rooms
    get_query = "SELECT * FROM rooms"
    if id:
        get_query += ' WHERE roomName = "{}"'.format(id)
    try:
        data = cur.execute(get_query)
        data = cur.fetchall()
    except Error as e:
        print(e)
    return data
    # print(cur.fetchall(), "Displaying  results from Room Table...")

# Get bounds for rooms id
@connect
def get_room_bound(cur):
    get_query = "Select count(*) from rooms;"
 

    try:
        data = cur.execute(get_query)
        data = cur.fetchall()
  
        # print(data)
        # print(cur.fetchall(), "Displaying  results from Exams Table...")

    except Error as e:
        print(e)
    return int(data[0][0])


# Delete specific Room details
@connect
def delete_room(cur, id=None):
    delete_query = "DELETE FROM rooms "
    if id:
        delete_query += ' WHERE roomName = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Rooms Table...")
        get_rooms(id = id)

    except Error as e:
        print(e)


# Update specific Room details
@connect
def update_room(cur, columnName, update, id=None):
    update_query = "UPDATE rooms SET "
    update_query += columnName
    update_query += ' = "{}"'.format(update)
    if id:
        update_query += 'WHERE roomName = "{}"'.format(id)

    try:
        cur.execute(update_query)

        print(cur.fetchall(), "Updating hits from Exams Table...")


    except Error as e:
        print(e)

if __name__ == '__main__':
    roomSize = 58
    alt = 32
    coord_longitude = "1223323"
    coord_latitude = "2223"
    name = "EHC_201"
    id = 12
    update = 40

    # insert_rooms(id = id, roomName= name,size=roomSize, alt=alt, coord_longitude = coord_longitude, coord_latitude=coord_latitude)
    # get_rooms()
    # get_rooms(id = name)
    # delete_room(id = name)

    # update_room(columnName = 'size', update = update, id = name)

    data = get_room_bound()
    print(data)

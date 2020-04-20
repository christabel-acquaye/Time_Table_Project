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
    cur.execute(get_query)

    print(cur.fetchall(), "Displaying  results from Room Table...")



# Delete specific Room details
@connect
def delete_exam(cur, id=None):
    delete_query = "DELETE FROM exams "
    if id:
        delete_query += ' WHERE roomName = "{}"'.format(id)

    try:
        cur.execute(delete_query)

        print(cur.fetchall(), "Displaying  deleted hits from Rooms Table...")


    except Error as e:
        print(e)



if __name__ == '__main__':
    size = 58
    alt = 32
    coord_longitude = "1223323"
    coord_latitude = "2223"
    name = "EHC_101"
    id = 3

    insert_rooms(id = id, roomName= name,size=size, alt=alt, coord_longitude = coord_longitude, coord_latitude=coord_latitude)
    # get_rooms()
    # get_rooms(id = name)




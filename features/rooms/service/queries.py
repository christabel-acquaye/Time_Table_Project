from _shared import in_query
from _shared.error_service import QUERY_NOT_FOUND


@in_query
def use_query(params: dict, query_type: str):
    query = ''

    if query_type == 'add-rooms':
        query = '''
            INSERT INTO rooms(id, roomName, size, alt, Coord_Longitude, Coord_Latitude)
            VALUES (
                %(id)s, %(roomName)s, %(size)s, %(alt)s , %(coord_longitude)s, %(coord_latitude)s
            )
        '''
    elif query_type == 'get-rooms':
        query = '''
           SELECT
                size,
                alt,
                id,
                roomName,
                coord_longitude,
                coord_latitude
            FROM rooms
        '''

        if params.get('id'):
            query += ' WHERE id = %(id)s'


        if params.get('roomName'):
            query += ' WHERE roomName = %(roomName)s'

    elif query_type == 'get-room-size':
        query = '''
            SELECT size from rooms WHERE roomName = %(roomName)s'
        '''
    else:
        raise QUERY_NOT_FOUND(query_type)

    return query

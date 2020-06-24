from .queries import use_query


def insert_rooms(id, roomName, size, alt, coord_longitude, coord_latitude):
    params = {
        'size': size,
        'alt': alt,
        'id': id,
        'roomName':  roomName,
        'coord_longitude':  coord_longitude,
        'coord_latitude':  coord_latitude
    }
    return use_query(params=params, query_type='add-rooms')


def get_rooms(id=None, roomName=None):
    params = {'id': id, 'roomName': roomName}
    return use_query(params=params, query_type='get-rooms')


def get_room_size(roomName):
    params = {
        'roomName': roomName
    }
    # return use_query(params =params, query_type ='get-room-size')
    return 200


def get_room_penalty(id):
    return 0


if __name__ == '__main__':
    from main import app
    with app.app_context():
        data = get_rooms()

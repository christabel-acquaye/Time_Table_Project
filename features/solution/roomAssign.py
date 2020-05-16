import math
import pprint

from sklearn.utils import shuffle

from _shared import NotEnoughRooms
from features.periods.service import get_periods
from features.rooms.service import get_rooms

from .services import get_exam_search

# Function that updates the room capacity after extracting the number of rooms to be used for a particular exam


def __update_room_capacity(room, capacity):
    return {**room, 'size': capacity}


def get_index_max_room_size(room_data):

    capacities = [room['size'] for room in room_data]

    return capacities.index(max(capacities))


def room_compute(current_student_size, room_data, room_allocated=None):
    if len(room_data) == 0:
        raise NotEnoughRooms

    room_allocated = room_allocated or []
    updated_room = room_data.copy()
    max_room_index = get_index_max_room_size(updated_room)
    room_capacity = room_data[max_room_index]['size']
    remainder = room_capacity - current_student_size

    if remainder < 0:
        room_allocated.append(updated_room[max_room_index])
        updated_room.pop(max_room_index)
        return room_compute(abs(remainder), updated_room.copy(), room_allocated)

    elif remainder > 0:
        updated_room[max_room_index] = __update_room_capacity(updated_room[max_room_index], remainder)

        room_allocated.append(__update_room_capacity(updated_room[max_room_index], room_capacity - remainder))

        return room_allocated, updated_room
    else:
        room_allocated.append(updated_room[max_room_index])
        updated_room.pop(max_room_index)
        return room_allocated, updated_room


# Function that returns the rooms available for a particular period
def period_room_allocation(periods, rooms):
    period_room = []
    periods = list(periods)
    room_arr = list(rooms)

    for period in periods:
        room_arr = shuffle(room_arr, random_state=0)
        period_room.append(room_arr)
    # pprint.pprint(period_room)
    return period_room


if __name__ == "__main__":
    T1 = [('A110', 200), ('RMA', 102), ('RMB', 103)]
    # print(type(T1))
    # room_allocated = []
    # room_compute(300, T1, room_allocated)

    # print(room)
    # print(result)
    # periods = get_period()
    from main import app
    with app.app_context():
        rooms = get_index_max_room_size(get_rooms())
    print(rooms)
    # period_room_allocation(periods, rooms)

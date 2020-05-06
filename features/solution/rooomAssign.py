import math
from features.solution.services import get_exam_search
from features.rooms.services import get_rooms
from sklearn.utils import shuffle
from features.periods.services import get_period
import pprint

def __update_room_capacity(room, capacity):
    return (room[0], room[1], capacity, room[3], room[4], room[5])


def room_compute(current_student_size, room_data, room_allocated = None):
    room_allocated = room_allocated or [] # the issue was from this
    
    updated_room = room_data.copy()
    room_capacity = room_data[0][2]
    remainder = room_capacity - current_student_size

    if remainder < 0:
        room_allocated.append(updated_room[0])
        updated_room.pop(0)
        
        return room_compute(abs(remainder), updated_room, room_allocated)

    elif remainder > 0:
        updated_room[0] = __update_room_capacity(updated_room[0], remainder)
        
        room_allocated.append(__update_room_capacity(updated_room[0], room_capacity - remainder))
        
        return room_allocated, updated_room
    else:
        room_allocated.append(updated_room[0])
        updated_room.pop(0)
        return room_allocated, updated_room
        



def period_room_allocation(periods, rooms):
    period_room = []
    periods = list(periods)
    room_arr = list(rooms)
    
    
    for period in periods:
        room_arr = shuffle(room_arr, random_state = 0)
        period_room.append(room_arr)
    # pprint.pprint(period_room)
    return period_room
    


if __name__ == "__main__":
    T1 = [('A110', 200), ('RMA', 102), ('RMB', 103)]
    # print(type(T1))
    room_allocated = []
    room_compute(300, T1, room_allocated)
    

    # print(room)
    # print(result) 
    # periods = get_period()
    # rooms = get_rooms()
    # period_room_allocation(periods, rooms)
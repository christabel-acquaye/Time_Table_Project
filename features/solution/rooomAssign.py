import math
from features.solution.services import get_exam_search
from features.rooms.services import get_rooms


def room_compute(current_student_size, room_data, room_allocated):
    updated_room = room_data
    # print(type(updated_room))
    room_capacity = room_data[0][1]
    
    remainder = room_capacity - current_student_size
    
    if remainder < 0:
        # print(updated_room[0])
        room_allocated.append(updated_room[0])
        # print(room_allocated)
        updated_room.pop(0)
        print(type(updated_room))
        return room_compute(abs(remainder), updated_room, room_allocated)

    elif remainder == 0:
        room_allocated.append(updated_room[0])
        updated_room.pop(0)
        return room_allocated, updated_room
        
    else:
        name, capacity = updated_room[0]
        updated_room[0] = (name, remainder)
        
        room_allocated.append((name, room_capacity - remainder))
        
        return room_allocated, updated_room




if __name__ == "__main__":
    T1 = [('A110', 200), ('RMA', 102), ('RMB', 103)]
    # print(type(T1))
    room_allocated = []
    room, result= room_compute(300, T1, room_allocated)


    print(room)
    print(result) 
    
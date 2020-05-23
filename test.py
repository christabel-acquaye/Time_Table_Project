from features.rooms.distance_services import get_distance_between_rooms


def find_average_distance(rooms):
    distances = []
    for i in len(rooms):
        distances.append(get_distance_between_rooms(rooms[i], rooms[i+1]))
    print(distances)


if __name__ == "__main__":
    roomA = ['EHC_101', 'NB_232', 'OLD_21']
    find_average_distance(roomA)

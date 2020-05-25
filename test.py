import datetime
import time

from features.rooms.distance_services import get_distance_between_rooms


def find_average_distance(rooms):
    distances = []
    for i in len(rooms):
        distances.append(get_distance_between_rooms(rooms[i], rooms[i+1]))
    print(distances)


# Sure
if __name__ == "__main__":
    # roomA = ['EHC_101', 'NB_232', 'OLD_21']
    # find_average_distance(roomA)
    f_date = '2020-05-22 00:00:00'
    l_date = '2020-06-04 00:00:00'
    print(get_date_difference(f_date, l_date))
    # convert it to a function which accepts a two dates and returns the difference, u might need it again

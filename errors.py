class NotEnoughRooms(Exception):
    def __init__(self, message='No rooms available to allocate students'):
        # Call the base class constructor with the parameters it needs
        super(NotEnoughRooms, self).__init__(message)



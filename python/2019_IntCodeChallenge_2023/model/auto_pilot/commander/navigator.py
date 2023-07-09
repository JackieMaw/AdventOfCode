class Navigator(Commander):
   
    def __init__(self, all_rooms):
        self._all_rooms = all_rooms

    def get_next_commands(self, room_description):
        raise NotImplementedError()
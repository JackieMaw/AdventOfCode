class Room:

    def __init__(self, name, doors, items, way_out):
        self.name = name
        self.doors = dict.fromkeys(doors, None)
        self.items = items
        self.way_out = way_out
        self.collected_items = False
    
    def connect_room(self, exit_door, next_room):
        self.doors[exit_door] = next_room


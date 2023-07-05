from model.autopilot.room_info import RoomInfo


ALL_DIRECTIONS = ["north", "south", "east", "west"]
OPPOSITE_DIRECTIONS = {"north": "south", "east" : "west", "south" : "north", "west" : "east"}

class Room:

    def __init__(self, room_info : RoomInfo):
        self._room_info = room_info
        self._all_doors = dict.fromkeys(room_info.doors, None)
        self._way_out = None
        self._collected_items = False

    def mark_entry(self, exit_door, previous_room):

        entry_door = OPPOSITE_DIRECTIONS[exit_door]
        self._all_doors[entry_door] = previous_room

        if self._way_out is None:
            self._way_out = entry_door
    
    def mark_exit(self, exit_door, next_room):
        self._all_doors[exit_door] = next_room

    def get_next_commands(self):
        next_commands = []
        if not self._collected_items:
            for item in self._room_info.items:
                next_commands.append(f"take {item}")
            self._collected_items = True
        next_door = self._get_next_door()
        next_commands.append(next_door)
        return next_commands
    
    def _get_next_door(self):        
        return next((door for (door, door_node) in self._all_doors.items() if door_node is None), self._way_out)
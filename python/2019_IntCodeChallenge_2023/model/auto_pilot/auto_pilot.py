from abc import ABC, abstractmethod
from model.auto_pilot.room import Room
from model.auto_pilot.room_parser import get_room_info

OPPOSITE_DIRECTIONS = {"north": "south", "east" : "west", "south" : "north", "west" : "east", None : None}
DANGEROUS_ITEMS = {"giant electromagnet", "infinite loop", "photons", "escape pod", "molten lava"}

class Commander(ABC):

    @abstractmethod
    def get_next_commands(self, room_description):
        pass



class Explorer(Commander):

    def __init__(self):
        self._all_rooms = {}
        self._previous_room = None
        self._previous_door = None

    def get_next_commands(self, room_description):

        (name, doors, items)  = get_room_info(room_description)

        if name in self._all_rooms:
            print(f"[Explorer] already seen this room: {name}")
            current_room = self._all_rooms[name]
        else:
            print(f"[Explorer] yay, a new room! {name}")
            way_out = OPPOSITE_DIRECTIONS[self._previous_door]
            current_room = Room(name, doors, items, way_out)
            
            self._connect_rooms(current_room)

            self._all_rooms[name] = current_room
        
        self._connect_rooms(current_room)

        commands = self._get_next_commands_for_room(current_room)

        self._previous_room = current_room 
        self._previous_door = commands[-1]

        print(f"[Explorer] next commands: {commands}")

        return commands
    
    def _connect_rooms(self, current_room):
        if self._previous_room is not None:
            self._previous_room.connect_room(current_room, self._previous_door)
            opposite_door = OPPOSITE_DIRECTIONS[self._previous_door]
            current_room.connect_room(self._previous_room, opposite_door)

    def _get_next_commands_for_room(self, current_room):
        next_commands = []
        if not current_room._collected_items:
            for item in current_room._room_info.items:
                if not self._is_dangerous(item):
                    next_commands.append(f"take {item}")
            current_room._collected_items = True
        next_door = self._get_next_door(current_room)
        next_commands.append(next_door)
        return next_commands
    
    def _get_next_door(self, current_room):
        if current_room._room_info.name == "Security Checkpoint":
            return current_room._way_out
        return next((door for (door, door_node) in current_room._all_doors.items() if door_node is None), current_room._way_out)
    
    def _is_dangerous(self, item):
        return item in DANGEROUS_ITEMS
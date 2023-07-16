import time
from model.auto_pilot.commander.commander import Commander
from model.auto_pilot.room import OPPOSITE_DIRECTIONS, Room
from model.auto_pilot.room_parser import get_room_info

DANGEROUS_ITEMS = {"giant electromagnet", "infinite loop", "photons", "escape pod", "molten lava"}

class Explorer(Commander):

    def __init__(self, all_rooms = {}, items = []):
        self._all_rooms = all_rooms
        self._items = items
        self._previous_room = None
        self._previous_door = None
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"logs\\explorer_summary_{timestr}.txt"

    def get_next_commands(self, room_description):

        (name, doors, items)  = get_room_info(room_description)

        if name in self._all_rooms:
            current_room = self._all_rooms[name]
        else:
            way_out = OPPOSITE_DIRECTIONS[self._previous_door]
            current_room = Room(name, doors, items, way_out)
            self._all_rooms[name] = current_room
        
        self._connect_rooms(current_room)

        commands = self._get_next_commands_for_room(current_room)

        self._previous_room = current_room
        self._previous_door = commands[-1]

        return commands
    
    def _connect_rooms(self, current_room : Room):
        if self._previous_room is not None:
            self._previous_room.connect_room(self._previous_door, current_room)
            self._write_to_file(f"{self._previous_room.name} >> {self._previous_door} >> {current_room.name}")

    def _write_to_file(self, s):
        with open(self._file_name, "a", encoding="utf-8") as file_handler:
            file_handler.write(s + "\n")

    def _get_next_commands_for_room(self, current_room : Room):
        next_commands = []
        if not current_room.collected_items:
            for item in current_room.items:
                if not self._is_dangerous(item):
                    next_commands.append(f"take {item}")
                    self._items.append(item)
            current_room.collected_items = True
        next_door = self._get_next_door(current_room)
        next_commands.append(next_door)
        return next_commands
    
    def _get_next_door(self, current_room : Room):
        if current_room.name == "Security Checkpoint":
            return current_room.way_out
        return next((door for (door, door_node) in current_room.doors.items() if door_node is None), current_room.way_out)
    
    def _is_dangerous(self, item):
        return item in DANGEROUS_ITEMS
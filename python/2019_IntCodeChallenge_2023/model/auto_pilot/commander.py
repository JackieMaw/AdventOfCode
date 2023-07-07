from abc import ABC, abstractmethod
import time
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
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"logs\\explorer_summary_{timestr}.txt"

    def get_next_commands(self, room_description):

        (name, doors, items)  = get_room_info(room_description)

        if name in self._all_rooms:
            print(f"[Explorer] already seen this room: {name}")
            current_room = self._all_rooms[name]
        else:
            print(f"[Explorer] yay, a new room! {name}")
            way_out = OPPOSITE_DIRECTIONS[self._previous_door]
            current_room = Room(name, doors, items, way_out)
            self._all_rooms[name] = current_room
        
        self._connect_rooms(current_room)

        commands = self._get_next_commands_for_room(current_room)

        self._previous_room = current_room 
        self._previous_door = commands[-1]

        print(f"[Explorer] next commands: {commands}")

        return commands
    
    def _connect_rooms(self, current_room : Room):
        if self._previous_room is not None:
            self._previous_room.connect_room(self._previous_door, current_room)
            opposite_door = OPPOSITE_DIRECTIONS[self._previous_door]
            current_room.connect_room(self._previous_room, opposite_door)
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

class Navigator(Commander):
    def get_next_commands(self, room_description):
        raise NotImplementedError()

class Juggler(Commander):
    def get_next_commands(self, room_description):
        raise NotImplementedError()

class CommanderOrchestrator(Commander):

    def __init__(self):
        self._all_commanders = [Explorer(), Navigator(), Juggler()]
    
    def get_next_commands(self, room_description):
        while len(self._all_commanders) > 0:
            current_commander = self._all_commanders[0]
            next_commands = current_commander.get_next_commands(room_description)
            if next_commands == [None]:
                self._all_commanders.pop(0)
                print(f"COMMANDER IS COMPLETE: {type(current_commander)}")
            else:
                return next_commands
        return None


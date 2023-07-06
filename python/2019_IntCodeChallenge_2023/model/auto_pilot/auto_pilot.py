from abc import ABC, abstractmethod
from model.auto_pilot.room import Room
from model.auto_pilot.room_info import RoomInfo


class CommandProvider(ABC):

    @abstractmethod
    def get_next_commands(self, room_description):
        pass

class AutoPilot(CommandProvider):

    def __init__(self):
        self._all_rooms = {}
        self._previous_room = None
        self._previous_door = None

    def get_next_commands(self, room_description):

        room_info = RoomInfo(room_description)

        if room_info.name in self._all_rooms:
            print(f"[AutoPilot] already seen this room: {room_info.name}")
            current_room = self._all_rooms[room_info.name]
        else:
            print(f"[AutoPilot] yay, a new room! {room_info.name}")
            current_room = Room(room_info)
            self._all_rooms[room_info.name] = current_room
        
        #if we travelled to this room from another room, we can mark the opposite door as already explored
        if self._previous_room is not None:
            current_room.mark_entry(self._previous_door, self._previous_room)
            self._previous_room.mark_exit(self._previous_door, current_room)

        commands = current_room.get_next_commands()

        self._previous_room = current_room
        self._previous_door = commands[-1]

        print(f"[AutoPilot] next commands: {commands}")

        return commands

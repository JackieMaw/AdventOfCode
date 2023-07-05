import time
from model.autopilot.room import Room
from model.autopilot.room_info import RoomInfo

from model.interaction_handler import InteractionHandler

class AutoPilotTranslator(InteractionHandler):
     
    def __init__(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"logs\\autopilot_log_{timestr}.txt"
        self._accumulated_output = []
        self._accumulated_input = []
        self._auto_pilot = AutoPilot()
    
    def provide_input(self):
        if len(self._accumulated_input) == 0:
            user_input = self._get_next_command()
            self._accumulated_input = list(user_input)
            self._accumulated_input.append(chr(10))
        single_input = self._accumulated_input.pop(0)
        self._write_to_file(single_input)
        return single_input

    def process_output(self, single_output):
        self._accumulated_output.append(single_output)
        self._write_to_file(single_output)
        print(single_output, end="")

    def _write_to_file(self, s):
        with open(self._file_name, "a", encoding="utf-8") as file_handler:
            file_handler.write(s)

    def _get_next_command(self):
        output = "".join(self._accumulated_output)
        self._accumulated_output = []
        return self._auto_pilot.get_commands(output)

class AutoPilot:

    def __init__(self):
        self._all_rooms = {}
        self._previous_room = None
        self._previous_door = None

    def get_commands(self, room_description):
        room_info = RoomInfo(room_description)

        if room_info.name in self._all_rooms:
            print("AutoPilot - already seen this room")
            current_room = self._all_rooms[room_info.name]
        else:
            print("AutoPilot - a new room!")
            current_room = Room(room_info)
            self._all_rooms[room_info.name] = current_room
        
        #if we travelled to this room from another room, we can mark the opposite door as already explored
        if self._previous_room is not None:
            current_room.mark_entry(_previous_door, _previous_room)
            _previous_room.mark_exit(_previous_door, current_room)

        self._previous_room = current_room
        commands = current_room.get_next_commands()

        print("AutoPilot - next commands:")
        print(commands)

        return commands

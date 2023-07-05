import time

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
        return self._auto_pilot.get_next_command(output)

class AutoPilot:

    def get_next_command(self, room_description):
        return "north"

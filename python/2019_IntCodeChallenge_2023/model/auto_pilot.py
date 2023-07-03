import time
from model.interaction_handler import InteractionHandler


class AutoPilot(InteractionHandler):
     
    def __init__(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"autopilot_log_{timestr}.txt"
        self._accumulated_output = []
        self._accumulated_input = []
    
    def provide_input(self):
        if len(self.accumulated_input) == 0:
            user_input = _get_next_command()
            self.accumulated_input = list(user_input)
            self.accumulated_input.append(chr(10))
        next_input = self.accumulated_input.pop(0)
        return next_input

    def process_output(self, int_code):
        output_to_send = chr(int_code)
        self._write_to_file(output_to_send)
        self._output_handler.send_output(output_to_send)

    def _write_to_file(self, s):
            with open(self._file_name, "a", encoding="utf-8") as file_handler:
                file_handler.write(s)

    def _get_next_command(self):
      return "north"
      
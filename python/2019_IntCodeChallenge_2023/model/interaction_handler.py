from abc import ABC
import time
from model.input_handler import PredefinedInputHandler, InputHandler, UserInputHandler
from model.output_handler import BasicOutputHandler, ConsoleOutputHandler, OutputHandler

class InteractionHandler(OutputHandler, InputHandler, ABC):
    @staticmethod
    def create_fixed_input(fixed_input, basic_output = []):
        return SimpleInteractionHandler(input_handler=PredefinedInputHandler(fixed_input), output_handler=BasicOutputHandler(basic_output), ascii_enabled=False)

class SimpleInteractionHandler(OutputHandler, InputHandler):

    def __init__(self, input_handler = UserInputHandler(), output_handler = ConsoleOutputHandler(), ascii_enabled = True, file_write = False):
        self._ascii_enabled = ascii_enabled
        self._input_handler = input_handler
        self._output_handler = output_handler
        self._file_write = file_write
        if file_write:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            self._file_name = f"interaction_log_{timestr}.txt"

    def get_input(self):
        input_received = self._input_handler.get_input()
        self._write_to_file(input_received)
        if self._ascii_enabled:
            return ord(input_received)
        else:
            return input_received

    def send_output(self, int_code):
        if self._ascii_enabled:
            output_to_send = chr(int_code)
        else:
            output_to_send = int_code
        self._write_to_file(output_to_send)
        self._output_handler.send_output(output_to_send)

    def _write_to_file(self, s):
        if self._file_write:
            with open(self._file_name, "a", encoding="utf-8") as file_handler:
                file_handler.write(s)

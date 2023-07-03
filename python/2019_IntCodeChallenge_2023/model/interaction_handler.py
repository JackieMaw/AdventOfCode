from abc import ABC
import time
from model.input_handler import PredefinedInputProvider, InputProvider, UserInputProvider
from model.output_handler import BasicOutputHandler, ConsoleOutputHandler, OutputHandler

class InteractionHandler(OutputHandler, InputProvider, ABC):
    @staticmethod
    def create_fixed_input(fixed_input, basic_output = []):
        return SimpleInteractionHandler(input_handler=PredefinedInputProvider(fixed_input), output_handler=BasicOutputHandler(basic_output))

class SimpleInteractionHandler(OutputHandler, InputProvider):

    def __init__(self, input_handler = UserInputProvider(), output_handler = ConsoleOutputHandler(), file_write = False):
        self._input_handler = input_handler
        self._output_handler = output_handler
        self._file_write = file_write
        if file_write:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            self._file_name = f"interaction_log_{timestr}.txt"

    def provide_input(self):
        input = self._input_handler.provide_input()
        self._write_to_file(input)
        return input

    def send_output(self, output):
        self._write_to_file(output)
        self._output_handler.send_output(output)

    def _write_to_file(self, s):
        if self._file_write:
            with open(self._file_name, "a", encoding="utf-8") as file_handler:
                file_handler.write(s)


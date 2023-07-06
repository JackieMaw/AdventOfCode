from abc import ABC
import time
from model.auto_pilot.auto_pilot import CommandProvider
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
            self._file_name = f"logs\\interaction_log_{timestr}.txt"

    def provide_input(self):
        next_input = self._input_handler.provide_input()
        self._write_to_file(next_input)
        return next_input

    def process_output(self, output):
        self._write_to_file(output)
        self._output_handler.process_output(output)

    def _write_to_file(self, s):
        if self._file_write:
            with open(self._file_name, "a", encoding="utf-8") as file_handler:
                file_handler.write(s)

class CommandInteractionHandler(InteractionHandler):
     
    def __init__(self, command_provider : CommandProvider):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"logs\\autopilot_log_{timestr}.txt"
        self._accumulated_output = []
        self._accumulated_input = []
        self._command_provider = command_provider
    
    def provide_input(self):
        if len(self._accumulated_input) == 0:
            next_commands = self._get_next_commands()
            for single_command in next_commands:
                self._accumulated_input += list(single_command)
                self._accumulated_input.append(chr(10))
        single_input = self._accumulated_input.pop(0)
        self._write_to_file(single_input)
        return single_input

    def process_output(self, output):
        self._accumulated_output.append(output)
        self._write_to_file(output)
        print(output, end="")

    def _write_to_file(self, s):
        with open(self._file_name, "a", encoding="utf-8") as file_handler:
            file_handler.write(s)

    def _get_next_commands(self):
        output = "".join(self._accumulated_output)
        self._accumulated_output = []
        return self._command_provider.get_next_commands(output)
from abc import ABC
import time
from model.input_handler import FixedInputHandler, InputHandler, UserInputHandler
from model.output_handler import BasicOutputHandler, ConsoleOutputHandler, OutputHandler

class Explorer(InteractionHandler):

    def __init__(self, input_handler = UserInputHandler(), output_handler = ConsoleOutputHandler()):
        self._input_handler = input_handler
        self._output_handler = output_handler
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"explorer_log_{timestr}.txt"

    def get_input(self):
        input_received = self._input_handler.get_input()
        self._write_to_file(input_received)
        return ord(input_received)

    def send_output(self, int_code):
        output_to_send = chr(int_code)
        self._write_to_file(output_to_send)
        self._output_handler.send_output(output_to_send)

    def _write_to_file(self, s):
        with open(self._file_name, "a", encoding="utf-8") as file_handler:
            file_handler.write(s)
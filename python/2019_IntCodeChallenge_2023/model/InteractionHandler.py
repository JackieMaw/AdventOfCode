import time
from model.InputStream import FixedInputStream, InputStream, UserInputStream
from model.OutputStream import BasicOutputStream, ConsoleOutputStream, OutputStream


class InteractionHandler(OutputStream, InputStream):

    def __init__(self, input_stream = UserInputStream(), output_stream = ConsoleOutputStream(), ascii_enabled = True, file_write = False):
        self._ascii_enabled = ascii_enabled
        self._input_stream = input_stream
        self._output_stream = output_stream
        self._file_write = file_write
        if file_write:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            self._file_name = f"input_output_{timestr}.txt"

    def receive(self):
        input_received = self._input_stream.receive()
        self._write_to_file(input_received)
        if self._ascii_enabled:
            return ord(input_received)
        else:
            return input_received

    def send(self, int_code):
        if self._ascii_enabled:
            output_to_send = chr(int_code)
        else:
            output_to_send = int_code
        self._write_to_file(output_to_send)
        self._output_stream.send(output_to_send)

    def _write_to_file(self, s):
        if self._file_write:
            with open(self._file_name, "a", encoding="utf-8") as file_stream:
                file_stream.write(s)

    def get_diagnostic_code(self):
        all_output = self._output_stream._all_output
        return all_output[len(all_output) - 1]

    @staticmethod
    def create_fixed_input(fixed_input, basic_output = []):
        return InteractionHandler(input_stream=FixedInputStream(fixed_input), output_stream=BasicOutputStream(basic_output), ascii_enabled=False)
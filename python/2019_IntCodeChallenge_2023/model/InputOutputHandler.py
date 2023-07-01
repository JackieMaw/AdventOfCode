import time
from model.InputStream import InputStream, UserInputStream
from model.OutputStream import ConsoleOutputStream, OutputStream
           

class InputOutputHandler(OutputStream, InputStream):

    def __init__(self, input_stream = UserInputStream(), output_stream = ConsoleOutputStream(), ascii_enabled = True):
        self._ascii_enabled = ascii_enabled
        self._input_stream = input_stream
        self._output_stream = output_stream
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self._file_name = f"input_output_{timestr}.txt"

    def receive(self):
        input_received = self._input_stream.receive()
        self.__write_to_file(input_received)
        if self._ascii_enabled:
            return ord(input_received)
        else:
            return input_received

    def send(self, int_code):
        if self._ascii_enabled:
            output_to_send = chr(int_code)
        else:
            output_to_send = int_code
        self.__write_to_file(output_to_send)
        self._output_stream.send(output_to_send)

    def __write_to_file(self, s):
        with open(self._file_name, "a", encoding="utf-8") as file_stream:
            file_stream.write(s)

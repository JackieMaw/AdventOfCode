from abc import ABC

class OutputHandler(ABC):
    def send_output(self, int_code):
        pass

class BasicOutputHandler(OutputHandler):
    
    def __init__(self, all_output = []):
        self._all_output = all_output

    def send_output(self, output):
        self._all_output.append(output)

class ConsoleOutputHandler(OutputHandler):

    def __init__(self, all_output = []):
        self._all_output = all_output

    def send_output(self, output):
        self._all_output.append(output)
        print(output, end="")
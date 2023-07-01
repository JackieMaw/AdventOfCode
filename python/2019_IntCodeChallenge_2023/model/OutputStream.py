from abc import ABC

class OutputStream(ABC):
    def send(self, int_code):
        pass

class ConsoleOutputStream(OutputStream):

    def __init__(self, all_output = []):
        self.all_output = all_output

    def send(self, output):
        self.all_output.append(output)
        print(output, end="")

    def get_ascii_output(self):  
        ascii_output = ''.join(self.all_output)
        ascii_output_no_empty_lines = [line for line in ascii_output.split("\n") if line]
        return ascii_output_no_empty_lines
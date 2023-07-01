from abc import ABC

class OutputStream(ABC):
    def append(self, int_code):
        pass

class OutputStreamDisplayAscii(OutputStream):

    all_output = []

    def append(self, int_code):
        output = chr(int_code)
        self.all_output.append(output)
        print(output, end="")

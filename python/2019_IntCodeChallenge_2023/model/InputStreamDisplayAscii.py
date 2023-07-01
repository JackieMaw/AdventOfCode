from abc import ABC

class InputStream(ABC):
    def pop(self, index):
        pass

class InputStreamDisplayAscii(InputStream):

    def __init__(self, ascii_lines):
        self.all_input = get_intcode_from_ascii(ascii_lines)

    def pop(self, index):
        int_code = self.all_input.pop(index)
        print(chr(int_code), end="")
        return int_code


def get_intcode_from_ascii(ascii):
    intcode = []
    for ascii_line in ascii:
        ascii_line = ",".join(ascii_line)
        for ascii_char in ascii_line:
            intcode.append(ord(ascii_char))
        intcode.append(10)
    return intcode
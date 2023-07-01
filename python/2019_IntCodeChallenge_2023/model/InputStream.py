from abc import ABC

class InputStream(ABC):
    def receive(self):
        pass

class UserInputStream(InputStream):

    def __init__(self):
        self.accumulated_input = []

    def receive(self):
        if len(self.accumulated_input) == 0:
            user_input = input(">> ")
            self.accumulated_input = list(user_input)
            self.accumulated_input.append(chr(10))
        next_input = self.accumulated_input.pop(0)

        return next_input

class FixedInputStream(InputStream):

    def __init__(self, all_input):
        self._all_input = all_input

    def receive(self):
        int_code = self._all_input.pop()
        #print(int_code, end="")
        return int_code


def get_intcode_from_ascii_enabled(ascii_enabled):
    intcode = []
    for ascii_enabled_line in ascii_enabled:
        ascii_enabled_line = ",".join(ascii_enabled_line)
        for ascii_enabled_char in ascii_enabled_line:
            intcode.append(ord(ascii_enabled_char))
        intcode.append(10)
    return intcode

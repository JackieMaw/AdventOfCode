from abc import ABC

class InputProvider(ABC):
    def provide_input(self):
        pass

class UserInputProvider(InputProvider):

    def __init__(self):
        self.accumulated_input = []

    def provide_input(self):
        if len(self.accumulated_input) == 0:
            user_input = input(">> ")
            self.accumulated_input = list(user_input)
            self.accumulated_input.append(chr(10))
        next_input = self.accumulated_input.pop(0)
        return next_input

class PredefinedInputProvider(InputProvider):

    def __init__(self, all_input):
        self._all_input = all_input

    @staticmethod
    def FromAsciiLines(ascii_lines):
        return PredefinedInputProvider(PredefinedInputProvider._get_input_from_ascii_lines(ascii_lines))

    def provide_input(self):
        if len(self._all_input) == 0:
            raise Exception("No Input Found")
        single_input = self._all_input.pop(0)
        print(single_input, end="")
        return single_input
    
    @staticmethod   
    def _get_input_from_ascii_lines(ascii_lines):
        all_input = []
        for ascii_line in ascii_lines:
            for ascii_char in ascii_line:
                all_input.append(ascii_char)
            all_input.append(chr(10))
        return all_input

from enum import Enum
from model.interaction_handler import InteractionHandler

class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2

class IntCodeComputer():
    def __init__(self):
        self._instruction_pointer = 0

    def execute(self, input_data):
        program_counter = 0

        while True:

            opcode = input_data[program_counter]

            if opcode == 99:
                break

            input1ptr = input_data[program_counter + 1]
            input1 = input_data[input1ptr]

            input2ptr = input_data[program_counter + 2]
            input2 = input_data[input2ptr]

            output = 0
            if opcode == 1:  #ADD
                output = input1 + input2
            elif opcode == 2:  #MULTIPLY
                output = input1 * input2

            output_ptr = input_data[program_counter + 3]
            input_data[output_ptr] = output

            program_counter += 4

        return input_data[0]
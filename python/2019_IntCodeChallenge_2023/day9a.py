#https://adventofcode.com/2019/day/9
#--- Day 9: Sensor Boost ---

from enum import Enum


class ParameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9
    TERMINATE = 99


class IntCodeComputer():
    def __init__(self, input_data, input_stream, output_stream):
        self.instruction_pointer = 0
        self.relative_base = 0
        self.memory_space = {}
        for memory_pointer in range(len(input_data)):
            self.memory_space[memory_pointer] = input_data[memory_pointer]
        self.input_stream = input_stream
        self.output_stream = output_stream

    def split_opcode(full_opcode):

        #The opcode is a two-digit number based only on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an instruction.

        opcode = full_opcode % 100

        #Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's mode is in the ten-thousands digit

        full_opcode_str = str(full_opcode)
        while len(full_opcode_str) < 5:
            full_opcode_str = "0" + full_opcode_str

        mode1 = int(full_opcode_str[2:3])
        mode2 = int(full_opcode_str[1:2])
        mode3 = int(full_opcode_str[0:1])

        return (OpCode(opcode), ParameterMode(mode1), ParameterMode(mode2),
                ParameterMode(mode3))

    def get_value(self, pointer, mode):

        param = self.memory_space[pointer]

        if mode == ParameterMode.IMMEDIATE_MODE:
            return param
        elif mode == ParameterMode.POSITION_MODE:
            return self.memory_space[param]
        elif mode == ParameterMode.RELATIVE_MODE:
            return self.memory_space[param + self.relative_base]
        else:
            raise Exception(f"Unsupported Parameter Mode: {mode}")

    def add(self, mode1, mode2, mode3):

        print(f"Add: {mode1} + {mode2}")

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Add: {value1} + {value2}")
        output = value1 + value2
        output_ptr = self.memory_space[self.instruction_pointer + 3]
        if mode3 == ParameterMode.RELATIVE_MODE:
            output_ptr = output_ptr + self.relative_base
        
        self.memory_space[output_ptr] = output

        self.instruction_pointer = self.instruction_pointer + 4

    def multiply(self, mode1, mode2):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Multiply: {value1} x {value2}")
        result = value1 * value2

        output_ptr = self.memory_space[self.instruction_pointer + 3]
        self.memory_space[output_ptr] = result

        self.instruction_pointer = self.instruction_pointer + 4

    def input(self):

        input_to_save = self.input_stream.pop(0)
        print(f"INPUT: {input_to_save}")
        output_ptr = self.memory_space[self.instruction_pointer + 1]
        self.memory_space[output_ptr] = input_to_save

        self.instruction_pointer = self.instruction_pointer + 2

    def output(self, mode1):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)

        print(f"OUTPUT: {value1}")
        self.output_stream.append(value1)

        self.instruction_pointer = self.instruction_pointer + 2

    def jump_if_true(self, mode1, mode2):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Jump-if-True: {value1} >> {value2}")
        if value1 != 0:
            self.instruction_pointer = value2
        else:
            self.instruction_pointer = self.instruction_pointer + 3

    def jump_if_false(self, mode1, mode2):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Jump-if-False: {value1} >> {value2}")
        if value1 == 0:
            self.instruction_pointer = value2
        else:
            self.instruction_pointer = self.instruction_pointer + 3

    def less_than(self, mode1, mode2):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Less Than: {value1} < {value2}")
        if value1 < value2:
            output = 1
        else:
            output = 0

        output_ptr = self.memory_space[self.instruction_pointer + 3]
        self.memory_space[output_ptr] = output

        self.instruction_pointer = self.instruction_pointer + 4

    def equals(self, mode1, mode2):

        value1 = self.get_value(self.instruction_pointer + 1, mode1)
        value2 = self.get_value(self.instruction_pointer + 2, mode2)

        print(f"Equals: {value1} == {value2}")
        if value1 == value2:
            output = 1
        else:
            output = 0

        output_ptr = self.memory_space[self.instruction_pointer + 3]
        self.memory_space[output_ptr] = output

        self.instruction_pointer = self.instruction_pointer + 4

    def adjust_relative_base(self):

        value1 = self.get_value(self.instruction_pointer + 1,
                                ParameterMode.IMMEDIATE_MODE)

        self.relative_base = self.relative_base + value1
        print(f"Adjust Relative Base by: {value1} ==> {self.relative_base}")

        self.instruction_pointer = self.instruction_pointer + 2

    def run_intcode(self):

        while True:

            full_opcode = self.memory_space[self.instruction_pointer]

            (opcode, mode1, mode2,
             mode3) = IntCodeComputer.split_opcode(full_opcode)

            if opcode == OpCode.TERMINATE:
                return_code = self.memory_space[0]
                print(f"Program Terminated. Return code: {return_code}")
                return return_code

            elif opcode == OpCode.ADD:
                self.add(mode1, mode2)

            elif opcode == OpCode.MULTIPLY:
                self.multiply(mode1, mode2)

            elif opcode == OpCode.INPUT:
                self.input()

            elif opcode == OpCode.OUTPUT:
                self.output(mode1)
            elif opcode == OpCode.JUMP_IF_TRUE:
                self.jump_if_true(mode1, mode2)

            elif opcode == OpCode.JUMP_IF_FALSE:
                self.jump_if_false(mode1, mode2)

            elif opcode == OpCode.LESS_THAN:
                self.less_than(mode1, mode2)

            elif opcode == OpCode.EQUALS:
                self.equals(mode1, mode2)

            elif opcode == OpCode.ADJUST_RELATIVE_BASE:
                self.adjust_relative_base()

            else:
                raise Exception(f"Unsupported OpCode: {opcode}")

        raise Exception("Unexpected end of program.")


def execute(input_data, input_stream, output_stream):
    computer = IntCodeComputer(input_data, input_stream, output_stream)
    computer.run_intcode()
    print(f"Diagnostic Test Completed.")
    print(f"All Outputs: {output_stream}")
    diagnostic_code = output_stream[len(output_stream) - 1]
    print(f"Diagnostic code: {diagnostic_code}")
    return diagnostic_code


def execute_all():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    result = execute(input_data, input_stream, output_stream)
    print(f" ==== ACTUAL Result: {result}  ====")

    assert result == 2369720
    print(f"ACTUAL PASSED!")

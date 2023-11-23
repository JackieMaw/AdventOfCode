from enum import Enum
from model.interaction_handler import InteractionHandler


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2

class IntCodeComputer():
    def __init__(self, interaction_handler : InteractionHandler, ascii_enabled = False):
        self._instruction_pointer = 0
        self._relative_base = 0
        self._memory_space = {}
        self._interaction_handler = interaction_handler
        self._ascii_enabled = ascii_enabled

    @staticmethod
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

        param = self._memory_space.get(pointer, 0)

        if mode == ParameterMode.IMMEDIATE_MODE:
            return param
        elif mode == ParameterMode.POSITION_MODE:
            return self._memory_space.get(param, 0)
        elif mode == ParameterMode.RELATIVE_MODE:
            return self._memory_space.get(param + self._relative_base, 0)
        else:
            raise Exception(f"Unsupported Parameter Mode: {mode}")

    def set_value(self, value, pointer, mode):

        param = self._memory_space[pointer]

        if mode == ParameterMode.POSITION_MODE:
            self._memory_space[param] = value
        elif mode == ParameterMode.RELATIVE_MODE:
            self._memory_space[param + self._relative_base] = value
        else:
            raise Exception(f"Unsupported Parameter Mode: {mode}")

    def add(self, mode1, mode2, mode3):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)

        result = value1 + value2
        #print(f"Add: {value1} + {value2} = {result}")

        self.set_value(result, self._instruction_pointer + 3, mode3)

        self._instruction_pointer = self._instruction_pointer + 4

    def multiply(self, mode1, mode2, mode3):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)

        result = value1 * value2
        #print(f"Multiply: {value1} x {value2} = {result}")

        self.set_value(result, self._instruction_pointer + 3, mode3)

        self._instruction_pointer = self._instruction_pointer + 4

    def get_input(self, mode1):

        input_to_save = self._interaction_handler.provide_input()

        if self._ascii_enabled:
            input_to_save = ord(input_to_save)
        #print(f"INPUT received: {input_to_save}")

        self.set_value(input_to_save, self._instruction_pointer + 1, mode1)

        self._instruction_pointer = self._instruction_pointer + 2

    def send_output(self, mode1):

        value_to_output = self.get_value(self._instruction_pointer + 1, mode1)

        if self._ascii_enabled:
            value_to_output = chr(value_to_output)

        #print(f"OUTPUT sent: {value_to_output}")
        self._interaction_handler.process_output(value_to_output)

        self._instruction_pointer = self._instruction_pointer + 2

    def jump_if_true(self, mode1, mode2):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)
        
        if value1 != 0:
            #print(f"Jump-if-True: {value1} = TRUE, instruction_pointer >> {value2} ")
            self._instruction_pointer = value2
        else:
            #print(f"Jump-if-True: {value1} = FALSE, NO JUMP")
            self._instruction_pointer = self._instruction_pointer + 3

    def jump_if_false(self, mode1, mode2):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)

        if value1 == 0:
            #print(f"Jump-if-False: {value1} = FALSE, instruction_pointer >> {value2} ")
            self._instruction_pointer = value2
        else:
            #print(f"Jump-if-False: {value1} = TRUE, NO JUMP")
            self._instruction_pointer = self._instruction_pointer + 3

    def less_than(self, mode1, mode2, mode3):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)

        if value1 < value2:
            #print(f"Less Than: {value1} < {value2} => TRUE(1)")
            result = 1
        else:
            #print(f"Less Than: {value1} < {value2} => FALSE(0)")
            result = 0
        
        self.set_value(result, self._instruction_pointer + 3, mode3)

        self._instruction_pointer = self._instruction_pointer + 4

    def equals(self, mode1, mode2, mode3):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)
        value2 = self.get_value(self._instruction_pointer + 2, mode2)

        #print(f"Equals: {value1} == {value2}")
        if value1 == value2:
            #print(f"Equals: {value1} == {value2} => TRUE(1)")
            result = 1
        else:
            #print(f"Equals: {value1} == {value2} => FALSE(0)")
            result = 0
        
        self.set_value(result, self._instruction_pointer + 3, mode3)

        self._instruction_pointer = self._instruction_pointer + 4

    def adjust_relative_base(self, mode1):

        value1 = self.get_value(self._instruction_pointer + 1, mode1)

        #print(f"Adjust Relative Base by: {value1}. {self.relative_base} ==> {self.relative_base + value1}")
        self._relative_base = self._relative_base + value1

        self._instruction_pointer = self._instruction_pointer + 2

    def _load_program_into_memory(self, intcode):
        for memory_pointer in range(len(intcode)):
            self._memory_space[memory_pointer] = intcode[memory_pointer]

    def run(self, intcode_program):

        self._load_program_into_memory(intcode_program)
        
        while True:

            full_opcode = self._memory_space[self._instruction_pointer]

            (opcode, mode1, mode2,
             mode3) = self.split_opcode(full_opcode)

            if opcode == OpCode.TERMINATE:
                return_code = self._memory_space[0]
                #print(f"Program Terminated. Return code: {return_code}")
                return return_code

            elif opcode == OpCode.ADD:
                self.add(mode1, mode2, mode3)

            elif opcode == OpCode.MULTIPLY:
                self.multiply(mode1, mode2, mode3)

            elif opcode == OpCode.INPUT:
                self.get_input(mode1)

            elif opcode == OpCode.OUTPUT:
                self.send_output(mode1)

            elif opcode == OpCode.JUMP_IF_TRUE:
                self.jump_if_true(mode1, mode2)

            elif opcode == OpCode.JUMP_IF_FALSE:
                self.jump_if_false(mode1, mode2)

            elif opcode == OpCode.LESS_THAN:
                self.less_than(mode1, mode2, mode3)

            elif opcode == OpCode.EQUALS:
                self.equals(mode1, mode2, mode3)

            elif opcode == OpCode.ADJUST_RELATIVE_BASE:
                self.adjust_relative_base(mode1)

            else:
                raise Exception(f"Unsupported OpCode: {opcode}")



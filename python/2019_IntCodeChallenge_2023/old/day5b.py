#https://adventofcode.com/2019/day/5
#--- Day 5: Sunny with a Chance of Asteroids ---

from enum import Enum


class ParameterMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    TERMINATE = 99


def init_memory(intcode_program):
    memory_space = {}
    for memory_pointer in range(len(intcode_program)):
        memory_space[memory_pointer] = intcode_program[memory_pointer]
    return memory_space


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


def add(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Add: {value1} + {value2}")
    output = value1 + value2
    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = output

    return instruction_pointer + 4


def multiply(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Multiply: {value1} x {value2}")
    result = value1 * value2

    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = result

    return instruction_pointer + 4


def input(instruction_pointer, memory_space, input_handler):

    input_to_save = input_handler.pop(0)
    print(f"INPUT: {input_to_save}")
    output_ptr = memory_space[instruction_pointer + 1]
    memory_space[output_ptr] = input_to_save

    return instruction_pointer + 2


def get_value(memory_space, pointer, mode):

    param = memory_space[pointer]

    if mode == ParameterMode.IMMEDIATE_MODE:
        return param
    elif mode == ParameterMode.POSITION_MODE:
        return memory_space[param]
    else:
        raise Exception(f"Unsupported Parameter Mode: {mode}")


def output(instruction_pointer, memory_space, output_handler, mode1):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)

    print(f"OUTPUT: {value1}")
    output_handler.append(value1)

    return instruction_pointer + 2


def jump_if_true(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Jump-if-True: {value1} >> {value2}")
    if value1 != 0:
        return value2
    else:
        return instruction_pointer + 3


def jump_if_false(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Jump-if-False: {value1} >> {value2}")
    if value1 == 0:
        return value2
    else:
        return instruction_pointer + 3


def less_than(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Less Than: {value1} < {value2}")
    if value1 < value2:
        output = 1
    else:
        output = 0

    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = output

    return instruction_pointer + 4


def equals(instruction_pointer, memory_space, mode1, mode2):

    value1 = get_value(memory_space, instruction_pointer + 1, mode1)
    value2 = get_value(memory_space, instruction_pointer + 2, mode2)

    print(f"Equals: {value1} == {value2}")
    if value1 == value2:
        output = 1
    else:
        output = 0

    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = output

    return instruction_pointer + 4


def run_intcode(intcode_program, input_handler, output_handler):

    memory_space = init_memory(intcode_program)

    instruction_pointer = 0
    while True:

        full_opcode = memory_space[instruction_pointer]

        (opcode, mode1, mode2, mode3) = split_opcode(full_opcode)

        if opcode == OpCode.TERMINATE:
            return_code = memory_space[0]
            print(f"Program Terminated. Return code: {return_code}")
            return return_code

        elif opcode == OpCode.ADD:
            instruction_pointer = add(instruction_pointer, memory_space, mode1,
                                      mode2)

        elif opcode == OpCode.MULTIPLY:
            instruction_pointer = multiply(instruction_pointer, memory_space,
                                           mode1, mode2)

        elif opcode == OpCode.INPUT:
            instruction_pointer = input(instruction_pointer, memory_space,
                                        input_handler)

        elif opcode == OpCode.OUTPUT:
            instruction_pointer = output(instruction_pointer, memory_space,
                                         output_handler, mode1)
        elif opcode == OpCode.JUMP_IF_TRUE:
            instruction_pointer = jump_if_true(instruction_pointer,
                                               memory_space, mode1, mode2)

        elif opcode == OpCode.JUMP_IF_FALSE:
            instruction_pointer = jump_if_false(instruction_pointer,
                                                memory_space, mode1, mode2)

        elif opcode == OpCode.LESS_THAN:
            instruction_pointer = less_than(instruction_pointer, memory_space,
                                            mode1, mode2)

        elif opcode == OpCode.EQUALS:
            instruction_pointer = equals(instruction_pointer, memory_space,
                                         mode1, mode2)

        else:
            raise Exception(f"Unsupported OpCode: {opcode}")

    raise Exception("Unexpected end of program.")


def execute(intcode_program, input_handler, output_handler):
    run_intcode(intcode_program, input_handler, output_handler)
    print(f"Diagnostic Test Completed. All Outputs: {output_handler}")
    diagnostic_code = output_handler[len(output_handler) - 1]
    return diagnostic_code


def test_input_output():
    test_data = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_handler = [expected_result]
    output_handler = []
    test_result = execute(test_data, input_handler, output_handler)
    assert test_result == expected_result


def execute_all():

    with open("./input/day5_actual.txt", "r") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    input_handler = [1]
    output_handler = []
    result = execute(intcode_program, input_handler, output_handler)
    print(f"REGRESSION Result: {result}")

    assert result == 13933662
    print(f"==== REGRESSION PASSED ====")

    input_handler = [5]
    output_handler = []
    result = execute(intcode_program, input_handler, output_handler)
    print(f" ==== ACTUAL Result: {result}  ====")

    assert result == 2369720
    print(f"ACTUAL PASSED!")

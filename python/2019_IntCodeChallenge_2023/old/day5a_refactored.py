#https://adventofcode.com/2019/day/5
#--- Day 5: Sunny with a Chance of Asteroids ---

POSITION_MODE = 0
IMMEDIATE_MODE = 1

ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4


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

    return (opcode, mode1, mode2, mode3)


def test_split_opcode():
    (opcode, mode1, mode2, mode3) = split_opcode(11001)
    assert opcode == 1
    assert mode1 == POSITION_MODE
    assert mode2 == IMMEDIATE_MODE
    assert mode3 == IMMEDIATE_MODE

    (opcode, mode1, mode2, mode3) = split_opcode(1002)
    assert opcode == 2
    assert mode1 == POSITION_MODE
    assert mode2 == IMMEDIATE_MODE
    assert mode3 == POSITION_MODE


def add(instruction_pointer, memory_space, mode1, mode2, mode3):

    input1ptr = memory_space[instruction_pointer + 1]
    if mode1 == 1:
        input1 = input1ptr
    else:
        input1 = memory_space[input1ptr]

    input2ptr = memory_space[instruction_pointer + 2]
    if mode2 == 1:
        input2 = input2ptr
    else:
        input2 = memory_space[input2ptr]

    print(f"Add: {input1} + {input2}")
    output = input1 + input2
    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = output

    return instruction_pointer + 4


def multiply(instruction_pointer, memory_space, mode1, mode2, mode3):

    input1ptr = memory_space[instruction_pointer + 1]
    if mode1 == 1:
        input1 = input1ptr
    else:
        input1 = memory_space[input1ptr]

    input2ptr = memory_space[instruction_pointer + 2]
    if mode2 == 1:
        input2 = input2ptr
    else:
        input2 = memory_space[input2ptr]

    print(f"Multiply: {input1} x {input2}")
    output = input1 * input2
    output_ptr = memory_space[instruction_pointer + 3]
    memory_space[output_ptr] = output

    return instruction_pointer + 4


def input(instruction_pointer, memory_space, input_stream):

    input_to_save = input_stream.pop(0)
    print(f"INPUT: {input_to_save}")
    output_ptr = memory_space[instruction_pointer + 1]
    memory_space[output_ptr] = input_to_save

    return instruction_pointer + 2


def output(instruction_pointer, memory_space, output_stream):

    output_ptr = memory_space[instruction_pointer + 1]
    output = memory_space[output_ptr]
    print(f"OUTPUT: {output}")
    output_stream.append(output)

    return instruction_pointer + 2


def run_intcode(intcode_program, input_stream, output_stream):

    memory_space = init_memory(intcode_program)

    instruction_pointer = 0
    while True:

        full_opcode = memory_space[instruction_pointer]

        (opcode, mode1, mode2, mode3) = split_opcode(full_opcode)

        if opcode == Operation.TERMINATE:
            return_code = memory_space[0]
            print(f"Program Terminated. Return code: {return_code}")
            return return_code

        if opcode == ADD:
            instruction_pointer = add(instruction_pointer, memory_space, mode1,
                                      mode2, mode3)

        elif opcode == MULTIPLY:
            instruction_pointer = multiply(instruction_pointer, memory_space,
                                           mode1, mode2, mode3)

        elif opcode == INPUT:
            instruction_pointer = input(instruction_pointer, memory_space,
                                        input_stream)

        elif opcode == OUTPUT:
            instruction_pointer = output(instruction_pointer, memory_space,
                                         output_stream)

        else:
            raise Exception(f"Unsupported OpCode: {opcode}")

    raise Exception("Unexpected end of program.")


def execute(intcode_program, input_stream, output_stream):
    run_intcode(intcode_program, input_stream, output_stream)
    print(f"Diagnostic Test Completed.")
    print(f"All Outputs: {output_stream}")
    diagnostic_code = output_stream[len(output_stream) - 1]
    print(f"Diagnostic code: {diagnostic_code}")
    return diagnostic_code


def run_all_tests():
    test_split_opcode()

    test_data = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_stream = [expected_result]
    output_stream = []
    test_result = execute(test_data, input_stream, output_stream)
    assert test_result == expected_result

    test_data = [int(l) for l in "1002,4,3,4,33".split(",")]
    test_result = run_intcode(test_data, [], [])
    assert test_result == 1002

    print(f"ALL TESTS PASSED!")


def execute_all():

    run_all_tests()
  
    with open("./input/day5_actual.txt", "r") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    result = execute(intcode_program, input_stream, output_stream)
    print(f"ACTUAL Result: {result}")
  
    assert result == 7157989  
    print(f"ACTUAL PASSED!")

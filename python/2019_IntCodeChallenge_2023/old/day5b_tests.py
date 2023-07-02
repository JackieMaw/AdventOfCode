#https://adventofcode.com/2019/day/5
#--- Day 5: Sunny with a Chance of Asteroids ---

from day5b import *


def test_split_opcode():
    (opcode, mode1, mode2, mode3) = split_opcode(11001)
    assert opcode == OpCode.ADD
    assert mode1 == ParameterMode.POSITION_MODE
    assert mode2 == ParameterMode.IMMEDIATE_MODE
    assert mode3 == ParameterMode.IMMEDIATE_MODE

    (opcode, mode1, mode2, mode3) = split_opcode(1002)
    assert opcode == OpCode.MULTIPLY
    assert mode1 == ParameterMode.POSITION_MODE
    assert mode2 == ParameterMode.IMMEDIATE_MODE
    assert mode3 == ParameterMode.POSITION_MODE


def test_add():

    memory_space = [0, 5, 6, 0]
    instruction_pointer = 0
    mode1 = ParameterMode.IMMEDIATE_MODE
    mode2 = ParameterMode.IMMEDIATE_MODE
    instruction_pointer = add(instruction_pointer, memory_space, mode1, mode2)

    assert instruction_pointer == 4
    assert memory_space == [11, 5, 6, 0]

    memory_space = [0, 4, 5, 0, 5, 6]
    instruction_pointer = 0
    mode1 = ParameterMode.POSITION_MODE
    mode2 = ParameterMode.POSITION_MODE
    instruction_pointer = add(instruction_pointer, memory_space, mode1, mode2)

    assert instruction_pointer == 4
    assert memory_space == [11, 4, 5, 0, 5, 6]


def test_input_output():
    test_data = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_handler = [expected_result]
    output_handler = []
    test_result = execute(test_data, input_handler, output_handler)
    assert test_result == expected_result


def test_comparison_position_mode():
    test_data = [
        int(l) for l in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
    ]
    test_result = execute(test_data, [0], [])
    assert test_result == 0
    test_result = execute(test_data, [1], [])
    assert test_result == 1


def test_comparison_immediate_mode():
    test_data = [
        int(l) for l in "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")
    ]
    test_result = execute(test_data, [0], [])
    assert test_result == 0
    test_result = execute(test_data, [1], [])
    assert test_result == 1


def test_jump():
    test_data = [
        int(l) for l in
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        .split(",")
    ]
    test_result = execute(test_data, [7], [])
    assert test_result == 999
    test_result = execute(test_data, [8], [])
    assert test_result == 1000
    test_result = execute(test_data, [9], [])
    assert test_result == 1001


def execute_all():

    # UNIT TESTS
    test_split_opcode()
    test_add()

    # INTEGRATION TESTS

    test_input_output()
    test_comparison_position_mode()
    test_comparison_immediate_mode()
    test_jump()

    print(f"==== ALL TESTS PASSED ====")

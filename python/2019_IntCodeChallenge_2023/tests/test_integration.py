#https://adventofcode.com/2019/day/9
#--- Day 9: Sensor Boost ---

from model.InputStream import FixedInputStream
from model.IntCodeComputer import IntCodeComputer
from model.InteractionHandler import InteractionHandler
from model.OutputStream import ConsoleOutputStream

def execute_diagnostic_test(intcode_program, fixed_input):

    basic_output = []
    interaction_handler = InteractionHandler.create_fixed_input(fixed_input, basic_output)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    diagnostic_code = basic_output[len(basic_output) - 1]
    return diagnostic_code

def test_input_output():
    intcode_program = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    diagnostic_code = execute_diagnostic_test(intcode_program, [expected_result])
    assert diagnostic_code == expected_result


def test_comparison_position_mode():
    intcode_program = [
        int(l) for l in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
    ]
    diagnostic_code = execute_diagnostic_test(intcode_program, [0])
    assert diagnostic_code == 0
    diagnostic_code = execute_diagnostic_test(intcode_program, [1])
    assert diagnostic_code == 1


def test_comparison_immediate_mode():
    intcode_program = [
        int(l) for l in "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")
    ]
    diagnostic_code = execute_diagnostic_test(intcode_program, [0])
    assert diagnostic_code == 0
    diagnostic_code = execute_diagnostic_test(intcode_program, [1])
    assert diagnostic_code == 1


def test_jump():
    intcode_program = [
        int(l) for l in
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        .split(",")
    ]
    diagnostic_code = execute_diagnostic_test(intcode_program, [7])
    assert diagnostic_code == 999
    diagnostic_code = execute_diagnostic_test(intcode_program, [8])
    assert diagnostic_code == 1000
    diagnostic_code = execute_diagnostic_test(intcode_program, [9])
    assert diagnostic_code == 1001


def test_copy_myself():
    intcode_program = [
        int(l) for l in
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
    ]

    basic_output = []
    interaction_handler = InteractionHandler.create_fixed_input([], basic_output)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    assert basic_output == intcode_program


def test_16_digit():
    intcode_program = [
        int(l) for l in "1102,34915192,34915192,7,4,7,99,0".split(",")
    ]
    diagnostic_code = execute_diagnostic_test(intcode_program, [])
    assert diagnostic_code == 1219070632396864

def test_large_number():
    intcode_program = [int(l) for l in "104,1125899906842624,99".split(",")]
    diagnostic_code = execute_diagnostic_test(intcode_program, [])
    assert diagnostic_code == 1125899906842624


def test_input_from_relative_base():

    intcode_program = [203, 2, 2, 3, 4, 5, 6, 7, 8]
    interaction_handler = InteractionHandler.create_fixed_input([99])
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)

    #print(computer.memory_space)

    assert computer.instruction_pointer == 2
    assert computer.memory_space == {
        0: 203,
        1: 2,
        2: 99,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8
    }
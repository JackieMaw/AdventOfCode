#https://adventofcode.com/2019/day/9
#--- Day 9: Sensor Boost ---

from model.IntCodeComputer import *

def test_input_output():
    program = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_stream = [expected_result]
    output_stream = []
    diagnostic_code = execute_diagnostic(program, input_stream, output_stream)
    assert diagnostic_code == expected_result


def test_comparison_position_mode():
    program = [
        int(l) for l in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
    ]
    diagnostic_code = execute_diagnostic(program, [0], [])
    assert diagnostic_code == 0
    diagnostic_code = execute_diagnostic(program, [1], [])
    assert diagnostic_code == 1


def test_comparison_immediate_mode():
    program = [
        int(l) for l in "3,3,1105,-1,9,1101,0,0,12,4,12,99,1".split(",")
    ]
    diagnostic_code = execute_diagnostic(program, [0], [])
    assert diagnostic_code == 0
    diagnostic_code = execute_diagnostic(program, [1], [])
    assert diagnostic_code == 1


def test_jump():
    program = [
        int(l) for l in
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        .split(",")
    ]
    diagnostic_code = execute_diagnostic(program, [7], [])
    assert diagnostic_code == 999
    diagnostic_code = execute_diagnostic(program, [8], [])
    assert diagnostic_code == 1000
    diagnostic_code = execute_diagnostic(program, [9], [])
    assert diagnostic_code == 1001


def test_copy_myself():
    test_program = [
        int(l) for l in
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
    ]
    output_stream = []
    computer = IntCodeComputer()
    computer.run(test_program, [], output_stream)
    assert computer.output_stream == test_program


def test_16_digit():
    program = [
        int(l) for l in "1102,34915192,34915192,7,4,7,99,0".split(",")
    ]
    diagnostic_code = execute_diagnostic(program, [], [])
    assert diagnostic_code == 1219070632396864

def test_large_number():
    program = [int(l) for l in "104,1125899906842624,99".split(",")]
    diagnostic_code = execute_diagnostic(program, [], [])
    assert diagnostic_code == 1125899906842624


def test_input_from_relative_base():

    program = [203, 2, 2, 3, 4, 5, 6, 7, 8]
    computer = IntCodeComputer()

    computer.run(program, [99], [])

    print(computer.memory_space)

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


def execute_diagnostic(program, input_stream, output_stream):
    computer = IntCodeComputer()
    computer.run(program, input_stream, output_stream)
    return computer.get_diagnostic_code()

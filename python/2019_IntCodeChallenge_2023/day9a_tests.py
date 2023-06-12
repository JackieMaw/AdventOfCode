#https://adventofcode.com/2019/day/9
#--- Day 9: Sensor Boost ---

from day9a import IntCodeComputer, ParameterMode, OpCode, execute


def test_split_opcode():
    (opcode, mode1, mode2, mode3) = IntCodeComputer.split_opcode(11001)
    assert opcode == OpCode.ADD
    assert mode1 == ParameterMode.POSITION_MODE
    assert mode2 == ParameterMode.IMMEDIATE_MODE
    assert mode3 == ParameterMode.IMMEDIATE_MODE

    (opcode, mode1, mode2, mode3) = IntCodeComputer.split_opcode(1002)
    assert opcode == OpCode.MULTIPLY
    assert mode1 == ParameterMode.POSITION_MODE
    assert mode2 == ParameterMode.IMMEDIATE_MODE
    assert mode3 == ParameterMode.POSITION_MODE

    (opcode, mode1, mode2, mode3) = IntCodeComputer.split_opcode(204)
    assert opcode == OpCode.OUTPUT
    assert mode1 == ParameterMode.RELATIVE_MODE
    assert mode2 == ParameterMode.POSITION_MODE
    assert mode3 == ParameterMode.POSITION_MODE


def test_add_immediate_mode():

    intcode_program = [0, 5, 6, 0]
    computer = IntCodeComputer(intcode_program, [], [])

    mode1 = ParameterMode.IMMEDIATE_MODE
    mode2 = ParameterMode.POSITION_MODE
    mode3 = ParameterMode.POSITION_MODE

    computer.add(mode1, mode2, mode3)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {0: 11, 1: 5, 2: 6, 3: 0}


def test_add_position_mode():

    intcode_program = [0, 4, 5, 0, 5, 6]
    computer = IntCodeComputer(intcode_program, [], [])

    mode1 = ParameterMode.POSITION_MODE
    mode2 = ParameterMode.POSITION_MODE
    mode3 = ParameterMode.POSITION_MODE

    computer.add(mode1, mode2, mode3)

    print(computer.memory_space)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {0: 11, 1: 4, 2: 5, 3: 0, 4: 5, 5: 6}


def test_add_relative_mode():

    intcode_program = [2203, 1, 2, 3, 0, 6, 6, 0]
    computer = IntCodeComputer(intcode_program, [], [])

    mode1 = ParameterMode.RELATIVE_MODE
    mode2 = ParameterMode.RELATIVE_MODE
    mode3 = ParameterMode.RELATIVE_MODE
    computer.relative_base = 5
    computer.add(mode1, mode2, mode3)

    print(computer.memory_space)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {
        0: 2203,
        1: 1,
        2: 2,
        3: 3,
        4: 0,
        5: 6,
        6: 6,
        7: 12
    }


def test_add():
    test_add_immediate_mode()
    test_add_position_mode()
    test_add_relative_mode()


def test_input_output():
    test_data = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_stream = [expected_result]
    output_stream = []
    test_result = execute(test_data, input_stream, output_stream)
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


def test_copy_myself():
    test_data = [
        int(l) for l in
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".split(",")
    ]
    test_result = execute(test_data, [], [])
    assert test_result == 109


def test_16_digit():
    test_data = [
        int(l) for l in "1102,34915192,34915192,7,4,7,99,0".split(",")
    ]
    test_result = execute(test_data, [], [])
    assert test_result == 1219070632396864


def test_large_number():
    test_data = [int(l) for l in "104,1125899906842624,99".split(",")]
    test_result = execute(test_data, [], [])
    assert test_result == 1125899906842624


def execute_all():

    # UNIT TESTS
    test_split_opcode()
    test_add()

    # INTEGRATION TESTS

    test_input_output()
    test_comparison_position_mode()
    test_comparison_immediate_mode()
    test_jump()
    test_16_digit()
    test_large_number()
    #test_copy_myself()

    print(f"==== ALL TESTS PASSED ====")

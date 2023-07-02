#https://adventofcode.com/2019/day/9
#--- Day 9: Sensor Boost ---

from model.intcode_computer import *

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
    computer = IntCodeComputer(None)
    computer._load_program_into_memory(intcode_program)

    mode1 = ParameterMode.IMMEDIATE_MODE
    mode2 = ParameterMode.IMMEDIATE_MODE
    mode3 = ParameterMode.POSITION_MODE

    computer.add(mode1, mode2, mode3)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {0: 11, 1: 5, 2: 6, 3: 0}


def test_add_position_mode():

    intcode_program = [0, 4, 5, 0, 5, 6]
    computer = IntCodeComputer(None)
    computer._load_program_into_memory(intcode_program)

    mode1 = ParameterMode.POSITION_MODE
    mode2 = ParameterMode.POSITION_MODE
    mode3 = ParameterMode.POSITION_MODE

    computer.add(mode1, mode2, mode3)

    print(computer.memory_space)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {0: 11, 1: 4, 2: 5, 3: 0, 4: 5, 5: 6}


def test_add_relative_mode():

    intcode_program = [22201, 1, 2, 3, 0, 0, 6, 6, 0]
    computer = IntCodeComputer(None)
    computer._load_program_into_memory(intcode_program)

    mode1 = ParameterMode.RELATIVE_MODE
    mode2 = ParameterMode.RELATIVE_MODE
    mode3 = ParameterMode.RELATIVE_MODE
    computer.relative_base = 5
    computer.add(mode1, mode2, mode3)

    print(computer.memory_space)

    assert computer.instruction_pointer == 4
    assert computer.memory_space == {
        0: 22201,
        1: 1,
        2: 2,
        3: 3,
        4: 0,
        5: 0,
        6: 6,
        7: 6,
        8: 12
    }


def test_input_from_relative_base():


    intcode_program = [203, 1, 2, 3, 4, 5, 6, 7, 8]
    computer = IntCodeComputer(InteractionHandler.create_fixed_input([999]))
    computer._load_program_into_memory(intcode_program)

    mode1 = ParameterMode.RELATIVE_MODE
    computer.relative_base = 5
    computer.input(mode1)

    #print(computer.memory_space)

    assert computer.instruction_pointer == 2
    assert computer.memory_space == {
        0: 203,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 999,
        7: 7,
        8: 8
    }
from model.intcode_computer import IntCodeComputer
from model.interaction_handler import InteractionHandler

def execute_diagnostic_test(intcode_program, fixed_input):

    basic_output = []
    interaction_handler = InteractionHandler.create_fixed_input(fixed_input, basic_output)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    diagnostic_code = basic_output[len(basic_output) - 1]
    return diagnostic_code

def test_execute_2a():

    with open("./input/day5_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    intcode_program[1] = 12
    intcode_program[2] = 2

    result = execute_diagnostic_test(intcode_program, [])
    assert result == 3706713

def test_execute_2b():

    with open("./input/day5_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute_diagnostic_test(intcode_program, [])
    assert result == 8609

def test_execute_5a():

    with open("./input/day5_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute_diagnostic_test(intcode_program, [1])

    assert result == 2377080455

def test_execute_5b():

    with open("./input/day5_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute_diagnostic_test(intcode_program, [2])

    assert result == 74917

def test_execute_9a():

    with open("./input/day9_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute_diagnostic_test(intcode_program, [1])

    assert result == 2377080455

def test_execute_9b():

    with open("./input/day9_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute_diagnostic_test(intcode_program, [2])

    assert result == 74917
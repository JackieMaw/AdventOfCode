from model.InputOutputHandler import InputOutputHandler
from model.InputStream import *
from model.IntCodeComputer import *
from model.OutputStream import *
from model.VacuumRobot import *

def get_diagnostic_code(output_stream):
    return output_stream[len(output_stream) - 1]

def test_execute_9a():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = FixedInputStream([1], ascii_enabled = False)
    output_stream = ConsoleOutputStream()
    computer = IntCodeComputer()
    computer.run(input_data, input_stream, output_stream)
    result = get_diagnostic_code(output_stream.all_output)

    assert result == 2377080455

def test_execute_9b():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = FixedInputStream([2], ascii_enabled = False)
    output_stream = ConsoleOutputStream()
    computer = IntCodeComputer()
    computer.run(input_data, input_stream, output_stream)
    result = get_diagnostic_code(output_stream.all_output)

    assert result == 74917


def test_execute_17a():

    with open("./input/day17_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    computer = IntCodeComputer()
    input_stream = FixedInputStream([])
    output_stream = ConsoleOutputStream()
    intput_output_handler = InputOutputHandler(input_stream, output_stream)
    computer.run(input_data, intput_output_handler, intput_output_handler)
    ascii_output = output_stream.get_ascii_output()

    vacuum_robot = VaccumRobot(ascii_output)
    sum_of_alignment_parameters = vacuum_robot.get_alignment_parameters()
    assert sum_of_alignment_parameters == 3448

def test_execute_17b():

    with open("./input/day17_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream_ascii = ["AABCCACBCB", "L4L4L6R10L6", "L12L6R10L6", "R8R10L6", "y"]

    #force the robot to wake up
    input_data[0] = 2
    computer = IntCodeComputer()
    input_stream = FixedInputStream(input_stream_ascii)
    output_stream = ConsoleOutputStream()
    computer.run(input_data, input_stream, output_stream)
    dust_collected = get_diagnostic_code(output_stream.all_output)
    assert dust_collected == 0

def test_execute_25a():

    with open("./input/day25_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    computer = IntCodeComputer()
    input_stream = UserInputStream()
    output_stream = ConsoleOutputStream()
    computer.run(input_data, input_stream, output_stream)

    assert False
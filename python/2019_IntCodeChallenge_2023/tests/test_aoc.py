from model.InputStreamDisplayAscii import InputStreamDisplayAscii
from model.IntCodeComputer import *
from model.OutputStreamDisplayAscii import OutputStreamDisplayAscii
from model.VacuumRobot import *

def test_execute_9a():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    computer = IntCodeComputer()
    computer.run(input_data, input_stream, output_stream)
    result = computer.get_diagnostic_code()

    assert result == 2377080455

def test_execute_9b():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [2]
    output_stream = []
    computer = IntCodeComputer()
    computer.run(input_data, input_stream, output_stream)
    result = computer.get_diagnostic_code()

    assert result == 74917


def test_execute_17a():

    with open("./input/day17_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    computer = IntCodeComputer()
    computer.run(input_data, [], [])
    ascii_output = computer.get_ascii_output()

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
    input_stream = InputStreamDisplayAscii(input_stream_ascii)
    output_stream = OutputStreamDisplayAscii()
    computer.run(input_data, input_stream, output_stream)
    dust_collected = computer.get_diagnostic_code()
    assert dust_collected == 0
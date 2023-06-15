import model.IntCodeComputer
import model.VacuumRobot

def test_execute_9a():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()
    result = computer.get_diagnostic_code()

    assert result == 2377080455

def test_execute_9b():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [2]
    output_stream = []
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()
    result = computer.get_diagnostic_code()

    assert result == 74917



def test_execute_17a():

    with open("./input/day17_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    computer = model.IntCodeComputer.IntCodeComputer(input_data, [], [])
    computer.run()
    ascii_output = computer.get_ascii_output()

    vacuum_robot = model.VacuumRobot.VaccumRobot(ascii_output)
    sum_of_alignment_parameters = vacuum_robot.get_alignment_parameters()
    assert sum_of_alignment_parameters == 3448
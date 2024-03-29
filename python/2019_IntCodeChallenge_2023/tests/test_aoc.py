from model.VacuumRobot import VaccumRobot
from model.ascii_helper import translate_to_ascii
from model.input_handler import PredefinedInputProvider
from model.intcode_computer import IntCodeComputer
from model.interaction_handler import CommandInteractionHandler, InteractionHandler, SimpleInteractionHandler
from model.auto_pilot.commander.commander_orchestrator import CommanderOrchestrator
from model.output_handler import BasicOutputHandler, ConsoleOutputHandler

def execute_diagnostic_test(intcode_program, fixed_input):

    basic_output = []
    interaction_handler = InteractionHandler.create_fixed_input(fixed_input, basic_output)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    diagnostic_code = basic_output[len(basic_output) - 1]
    return diagnostic_code

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


def test_execute_17a():

    with open("./input/day17_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    input_handler = PredefinedInputProvider([])
    output_handler = BasicOutputHandler()
    interaction_handler = SimpleInteractionHandler(input_handler, output_handler)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    ascii_output = translate_to_ascii(output_handler._all_output)

    vacuum_robot = VaccumRobot(ascii_output)
    sum_of_alignment_parameters = vacuum_robot.get_alignment_parameters()
    assert sum_of_alignment_parameters == 3448

def test_execute_17b():

    with open("./input/day17_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    input_handler_ascii = ["AABCCACBCB", "L4L4L6R10L6", "L12L6R10L6", "R8R10L6", "y"]

    #force the robot to wake up
    intcode_program[0] = 2
    input_handler = PredefinedInputProvider(input_handler_ascii)
    basic_output = []
    output_handler = ConsoleOutputHandler(basic_output)
    interaction_handler = SimpleInteractionHandler(input_handler, output_handler)
    computer = IntCodeComputer(interaction_handler)
    computer.run(intcode_program)
    diagnostic_code = basic_output[len(basic_output) - 1]
    assert diagnostic_code == 0

def test_execute_25a():

    with open("./input/day25_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    assert False

    interaction_handler = CommandInteractionHandler(CommanderOrchestrator())
    computer = IntCodeComputer(interaction_handler, ascii_enabled = True)
    computer.run(intcode_program)
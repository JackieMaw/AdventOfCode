from model.input_handler import FixedInputHandler
from model.intcode_computer import IntCodeComputer
from model.interaction_handler import SimpleInteractionHandler

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

fixed_instruction_set = ["north", "north", "east"]
interaction_handler = SimpleInteractionHandler(input_handler=FixedInputHandler.FromAscii(fixed_instruction_set), file_write=True)
computer = IntCodeComputer(interaction_handler)
computer.run(intcode_program)

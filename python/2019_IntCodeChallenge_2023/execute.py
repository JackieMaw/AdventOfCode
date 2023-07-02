from model.interaction_handler import InteractionHandler
from model.intcode_computer import IntCodeComputer

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

interaction_handler = InteractionHandler()
computer = IntCodeComputer(interaction_handler)
computer.run(intcode_program)

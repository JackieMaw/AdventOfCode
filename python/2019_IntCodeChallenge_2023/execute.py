from model.InteractionHandler import InteractionHandler
from model.IntCodeComputer import IntCodeComputer

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

computer = IntCodeComputer(interaction_handler)
input_output_handler = InteractionHandler()
computer.run(intcode_program, input_output_handler, input_output_handler)

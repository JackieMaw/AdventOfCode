from model.explorer import Explorer
from model.intcode_computer import IntCodeComputer

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

interaction_handler = Explorer()
computer = IntCodeComputer(interaction_handler)
computer.run(intcode_program)

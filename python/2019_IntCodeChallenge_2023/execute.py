from model.InputOutputHandler import InputOutputHandler
from model.IntCodeComputer import IntCodeComputer

with open("./input/day25_actual.txt", "r") as text_file:
    input_data = [int(l) for l in text_file.read().split(",")]

computer = IntCodeComputer()
input_output_handler = InputOutputHandler()
computer.run(input_data, input_output_handler, input_output_handler)

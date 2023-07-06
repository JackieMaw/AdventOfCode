from model.autopilot.auto_pilot import AutoPilotTranslator
from model.input_handler import PredefinedInputProvider, UserInputProvider
from model.intcode_computer import IntCodeComputer
from model.interaction_handler import SimpleInteractionHandler

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

print("=====================")
print("Shall we play a game?")
print("=====================")
print("Mode 1 = Play Manual")
print("Mode 2 = With Predefined Instructions")
print("Mode 3 = Auto-pilot")
mode = input("Choose your mode: 1/2/3 >> ")

if mode == "1":
    interaction_handler = SimpleInteractionHandler(input_handler=UserInputProvider(), file_write=True)
elif mode == "2":
    predefined_input = input("Enter commands separated by commas >> ").split(",")
    interaction_handler = SimpleInteractionHandler(input_handler=PredefinedInputProvider.FromAsciiLines(predefined_input), file_write=True)
elif mode == "3":
    interaction_handler = AutoPilotTranslator()
else:
    assert False, "Invalid Mode: " + mode

computer = IntCodeComputer(interaction_handler, ascii_enabled = True)
computer.run(intcode_program)

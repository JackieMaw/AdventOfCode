from model.input_handler import PredefinedInputHandler, UserInputHandler
from model.intcode_computer import IntCodeComputer
from model.interaction_handler import SimpleInteractionHandler

with open("./input/day25_actual.txt", "r") as text_file:
    intcode_program = [int(l) for l in text_file.read().split(",")]

print("==================")
print("Let's Play a Game!")
print("==================")
print("Mode 1 = Play Manual")
print("Mode 2 = With Predefined Instructions")
print("Mode 3 = Auto-pilot")
mode = input("Choose your mode: 1/2/3 >> ")

if mode == "1":
    interaction_handler = SimpleInteractionHandler(input_handler=UserInputHandler(), file_write=True)
elif mode == "2":
    predefined_input = ["north", "north", "east"]
    interaction_handler = SimpleInteractionHandler(input_handler=PredefinedInputHandler.FromAscii(predefined_input), file_write=True)
elif mode == "3":
    predefined_input = ["north", "north", "east"]
    interaction_handler = SimpleInteractionHandler(input_handler=PredefinedInputHandler.FromAscii(predefined_input), file_write=True)
else:
    assert False, "Invalid Mode: " + mode

computer = IntCodeComputer(interaction_handler)
computer.run(intcode_program)

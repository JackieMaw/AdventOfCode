#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *

def execute(input):
    horiz = 0
    depth = 0

    for instruction in input:
        instruction_parts = instruction.split()
        dir = instruction_parts[0]
        num = int(instruction_parts[1])
        if dir == "forward":
            horiz += num         
        elif dir == "down":            
            depth += num
        elif dir == "up":
            depth -= num

    return horiz * depth

# TESTS
assert execute(get_strings(["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"])) == 150
print("ALL TESTS PASSED")

# REAL INPUT DATA
YEAR = 2021
DAY = 2
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
print(execute(input))
assert execute(input) == 1580000
print("ANSWER CORRECT")
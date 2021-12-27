#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def load(input):

    east, south = set()

    width = len(input[0])
    depth = len(input)

    for d in range(depth):
        line = input[d]
        for w in range(width):
            char = line[w]
            if char == ">":
                east.add((w, d))
            elif char == "v":
                south.add((w, d))

    return east, south, width, depth

def play(east, south, width, depth):

    num_moved = 0

    new_east = east.copy()
    for current_position in east:
        (w, d) = current_position
        new_w = 0 if w == width else w + 1
        new_position = (new_w, d)
        
        if new_position not in east and new_position not in south:
            new_east.remove(current_position)
            new_east.add(new_position)
            num_moved += 1
    east = new_east
    
    new_south = south.copy()
    for current_position in south:
        (w, d) = current_position
        new_d = 0 if d == depth else d + 1
        new_position = (w, new_d)
        
        if new_position not in east and new_position not in south:
            new_south.remove(current_position)
            new_south.add(new_position)
            num_moved += 1
    south = new_south

def execute(input):
    print(input)

    state = load(input)

    num_moved = 1
    iterations = 0
    while num_moved > 0:
        num_moved = play(state)
        iterations += 1

    result = iterations
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 25

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 58
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
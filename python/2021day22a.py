#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def get_range(string):    
    line_parts = string.split("..")
    start = max(int(line_parts[0][2:]), -50)
    end = min(int(line_parts[1]), 50)
    return (start, end)

#on x=-20..26,y=-36..17,z=-47..7
def initialize(space, line):

    switch_on = line[:2] == "on"

    line_parts = line.split(" ")[1].split(",")
    x_range = get_range(line_parts[0])
    y_range = get_range(line_parts[1])
    z_range = get_range(line_parts[2])

    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in range(z_range[0], z_range[1] + 1):
                cube = (x, y, z)
                if switch_on:
                    space.add(cube)
                else:
                    if cube in space:
                        space.remove(cube)                    

def execute(input):
    #print(input)

    space = set()
    for line in input:
        initialize(space, line)
        #size = len(space)
        #print(f"size: {size}")

    result = len(space)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 22

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 39

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 590784
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 647076
print("ANSWER CORRECT")
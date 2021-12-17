#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):
    print(input)
    result = 0
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 17

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# target area: x=20..30, y=-10..-5
assert execute(x1 = 20, x2 = 30, y1 =-10, y2 =-5) == 45
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# target area: x=207..263, y=-115..-63
assert execute(x1 = 207, x2 = 263, y1 =-115, y2 =-63) == 0
print("ANSWER CORRECT")
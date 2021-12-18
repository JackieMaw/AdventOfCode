#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def get_next_pos(pos, velocity):
    # TODO
    return pos

def hit_target(pos, target):
    # TODO
    return False

def missed(pos, target):
    # TODO
    return True

def will_hit_target_area(velocity, target):
    max_height = 0
    pos = (0, 0)
    still_possible = True
    while (still_possible):
        pos = get_next_pos(pos, velocity)
        (x, y) = pos
        if y > max_height:
            max_height = y
        if hit_target(pos, target):
            return True, max_height
        if missed(pos, target):
            return False, -1

def execute(x1, x2, y1, y2):
    max_height = 0
    velocity = 1
    success_in_past = False
    still_possible = True
    while still_possible:
        success, max_height_for_this_velocity = will_hit_target(velocity, target)
        if success and max_height_for_this_velocity > max_height:
            max_height = max_height_for_this_velocity
        still_possible

    print(input)
    result = max_height
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
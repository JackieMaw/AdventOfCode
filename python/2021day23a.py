#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy



def get_possible_moves():
    possible_moves = []

    # 1. Are there any players in the top of a room which can go home now?
    # 
    # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room
    # Amphipods will never move from the hallway into a room unless that room is their destination room 
    #   and that room contains no amphipods which do not also have that room as their own destination.

    # 2. Are there any players in the hallway which can go home?
    # 
    # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room
    # Amphipods will never move from the hallway into a room unless that room is their destination room 
    #   and that room contains no amphipods which do not also have that room as their own destination.
    
    # 2. For each room, does the top player in the room need to move? There are 7 possible spaces in the hallway it can move to.
    # 
    # Amphipods will never stop on the space immediately outside any room.
    # Amphipods will never move from the hallway into a room unless that room is their destination room 
    #   and that room contains no amphipods which do not also have that room as their own destination.

    return possible_moves

def execute(input):
    print(input)
    result = 0
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 23

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
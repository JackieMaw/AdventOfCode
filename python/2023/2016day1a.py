from utilities import *
import math
import copy

from enum import Enum
Direction = Enum('Direction', ['North', 'East', 'South', 'West'])


def turn(direction, next_turn):
    if next_turn == 'R':
        return turn_right(direction)
    elif next_turn == 'L':
        return turn_left(direction)
    else:
        raise Exception("Unexpected Turn: " + next_turn)

def turn_right(direction):
    if direction == Direction.North:
        return Direction.East
    elif direction == Direction.East:
        return Direction.South
    elif direction == Direction.South:
        return Direction.West
    elif direction == Direction.West:
        return Direction.North
    else:
        raise Exception("Unexpected Direction: " + direction)
    
def turn_left(direction):
    if direction == Direction.North:
        return Direction.West
    elif direction == Direction.West:
        return Direction.South
    elif direction == Direction.South:
        return Direction.East
    elif direction == Direction.East:
        return Direction.North
    else:
        raise Exception("Unexpected Direction: " + direction)

def move(x, y, direction, num_blocks):
    if direction == Direction.North:
        return (x + num_blocks, y)
    elif direction == Direction.East:
        return (x, y + num_blocks)
    elif direction == Direction.South:
        return (x - num_blocks, y)
    elif direction == Direction.West:
        return (x, y - num_blocks)


def execute(input):
    print(input)

    direction = Direction.North

    x = 0
    y = 0

    for instruction in input:
        next_turn = instruction[0]
        num_blocks = int(instruction[1:])
        direction = turn(direction, next_turn)

        print(f'{instruction} ==> ({x},{y}) move {direction} x {num_blocks}')
        (x, y) = move(x, y, direction, num_blocks)

    result = abs(x) + abs(y)
    print(f"result: {result}")
    return result
    

# TESTS
assert execute(get_strings_csv(["R2, L3"])) == 5
assert execute(get_strings_csv(["R2, R2, R2"])) == 2
assert execute(get_strings_csv(["R5, L5, R5, R3"])) == 12
print("ALL TESTS PASSED")

YEAR = 2016
DAY = 1

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings_csv(raw_input)
assert execute(input) == 243
print("ANSWER CORRECT")
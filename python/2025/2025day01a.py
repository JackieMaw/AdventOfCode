from utilities import *
import math
import copy

YEAR = 2025
DAY = 1
PART = 'a'

def assertt(actual, expected):
    assert actual == expected, f"Expected {expected}, but got {actual}"

def move(counter, direction, distance):
    if direction == 'L':
        counter -= int(distance)
        counter = counter % 100
    elif direction == 'R':
        counter += int(distance)
        counter = counter % 100
    else:
        raise ValueError(f"Unexpected direction: {direction}")
    return counter

def execute(puzzle_input):

    num_times_zero = 0

    counter = 50

    for input_line in puzzle_input:
        direction = input_line[0]
        distance = input_line[1:]
        counter = move(counter, direction, distance)
        if counter == 0:
            num_times_zero += 1  

    result = num_times_zero
    print(f"result: {result}")
    return result

# TESTS
assertt(move(50, 'L', 1), 49)
assertt(move(50, 'R', 1), 51)
assertt(move(50, 'R', 49), 99)
assertt(move(50, 'R', 50), 0)
assertt(move(50, 'L', 50), 0)
assertt(move(50, 'L', 51), 99)
print("ALL TESTS PASSED")

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
string_input = get_strings(raw_input)
result = execute(string_input)
expected_result = get_expected_result(YEAR, DAY, PART, "_test")
assertt(result, expected_result)
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
string_input = get_strings(raw_input)
result = execute(string_input)
expected_result = get_expected_result(YEAR, DAY, PART)
assertt(result, expected_result)
print("FULL INPUT PASSED")

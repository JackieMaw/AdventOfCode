from utilities import *
import math
import copy
import numpy

def parse_input(input_lines):
    grid = [[int(num) for num in line.split()] for line in input_lines]
    return grid

def solve(initial_state):
    return sum([extrapolate(row) for row in initial_state])

def get_differences(nums):
    return [nums[i+1] - nums[i] for i in range(len(nums) - 1)]    

def extrapolate(nums):
    all_zeros = not numpy.array(nums).any()
    if all_zeros:
        return 0
    else:
        return nums[-1] + extrapolate(get_differences(nums))

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS
assert extrapolate([0, 0, 0, 0]) == 0
assert extrapolate([3, 3, 3, 3, 3]) == 3
assert extrapolate([0, 3, 6, 9, 12]) == 15
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 9

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 114
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 1702218515
print("ANSWER CORRECT")
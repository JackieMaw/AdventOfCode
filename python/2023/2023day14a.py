from utilities import *
import math
import copy

def parse_input(input_lines):
    return []

def solve(initial_state):
    return -1

def get_load(line, scaling_factor):
    return line.count("O") * scaling_factor

def get_total_load(grid):
    num_lines = len(grid)
    return sum([get_load(line, num_lines - line_number) for line_number, line in enumerate(grid)])

def move_next_marble_north(grid, row_num, col_num):

    for r in range(row_num + 1, len(grid)):
        char = grid[r][col_num]
        if char == "O":
            grid[row_num][col_num] = "O"
            grid[r][col_num] = "."
            return
        elif char == '#':
            return

def roll_north(input_lines):
    grid = [ list(line) for line in input_lines ]

    for row_num in range(len(grid)):
        for col_num in range(len(grid[0])):
            if grid[row_num][col_num] == ".":
                move_next_marble_north(grid, row_num, col_num)

    return grid

def execute(grid):
    print(grid)
    grid = roll_north(grid)
    result = get_total_load(grid)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 14

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 136
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 108826
print("ANSWER CORRECT")
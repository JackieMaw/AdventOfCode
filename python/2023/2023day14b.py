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
        
def move_next_marble_south(grid, row_num, col_num):

    for r in range(row_num - 1, -1):
        char = grid[r][col_num]
        if char == "O":
            grid[row_num][col_num] = "O"
            grid[r][col_num] = "."
            return
        elif char == '#':
            return
        
def move_next_marble_west(grid, row_num, col_num):

    for c in range(col_num + 1, len(grid[0])):
        char = grid[row_num][c]
        if char == "O":
            grid[row_num][col_num] = "O"
            grid[row_num][c] = "."
            return
        elif char == '#':
            return

def move_next_marble_east(grid, row_num, col_num):

    for c in range(col_num - 1, -1):
        char = grid[row_num][c]
        if char == "O":
            grid[row_num][col_num] = "O"
            grid[row_num][c] = "."
            return
        elif char == '#':
            return

def roll_north(grid):
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == ".":
                move_next_marble_north(grid, row_num, col_num)

def roll_south(grid):
    for row_num in range(len(grid), -1):
        for col_num, char in enumerate(grid[row_num]):
            if char == ".":
                move_next_marble_south(grid, row_num, col_num)

def display_matrix(matrix):
    for row in matrix:
        print(' '.join([str(col) for col in row]))

def roll_west(grid):
    for col_num in range(len(grid[0])):
        for row_num in range(len(grid)):
            if grid[row_num][col_num] == ".":
                move_next_marble_west(grid, row_num, col_num)

def roll_east(grid):
    for col_num in range(len(grid[0]), -1):
        for row_num in range(len(grid)):
            if grid[row_num][col_num] == ".":
                move_next_marble_east(grid, row_num, col_num)

def spin(grid):
    print("BEFORE SPIN>>>")
    display_matrix(grid)
    roll_north(grid)
    print("AFTER ROLL NORTH:")
    display_matrix(grid)
    roll_west(grid)
    print("AFTER ROLL WEST")
    display_matrix(grid)
    roll_south(grid)
    print("AFTER ROLL SOUTH")
    display_matrix(grid)
    roll_east(grid)
    print("AFTER ROLL EAST")
    display_matrix(grid)

def execute(input_lines):
    
    print(input_lines)
    grid = [ list(line) for line in input_lines ]
    print(grid)
    
    #for _ in range(1000000000):
    for _ in range(1):
        spin(grid)

    result = get_total_load(grid)
    print(f"result: {result}")
    return result

# TESTS
test_grid = [['.', '.', '.'], ['.', 'O', '.'], ['.', '.', '.']]
roll_north(test_grid)
assert test_grid == [['.', 'O', '.'], ['.', '.', '.'], ['.', '.', '.']]
test_grid = [['.', '.', '.'], ['.', 'O', '.'], ['.', '.', '.']]
roll_south(test_grid)
assert test_grid == [['.', '.', '.'], ['.', '.', '.'], ['.', 'O', '.']]
test_grid = [['.', '.', '.'], ['.', 'O', '.'], ['.', '.', '.']]
roll_west(test_grid)
assert test_grid == [['.', '.', '.'], ['O', '.', '.'], ['.', '.', '.']]
test_grid = [['.', '.', '.'], ['.', 'O', '.'], ['.', '.', '.']]
roll_east(test_grid)
assert test_grid == [['.', '.', '.'], ['.', '.', 'O'], ['.', '.', '.']]
print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 14

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 0
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 108826
print("ANSWER CORRECT")
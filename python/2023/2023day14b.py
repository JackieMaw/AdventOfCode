from utilities import *
import math
import copy

spin_cache = {}

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
            #print(f"moved north from ({r, col_num}) to ({row_num, col_num})")
            grid[row_num][col_num] = "O"
            grid[r][col_num] = "."
            return
        elif char == '#':
            return
        
def move_next_marble_south(grid, row_num, col_num):

    for r in range(row_num - 1, -1, -1):
        char = grid[r][col_num]
        if char == "O":
            #print(f"moved south from ({r, col_num}) to ({row_num, col_num})")
            grid[row_num][col_num] = "O"
            grid[r][col_num] = "."
            return
        elif char == '#':
            return
        
def move_next_marble_west(grid, row_num, col_num):

    for c in range(col_num + 1, len(grid[0])):
        char = grid[row_num][c]
        if char == "O":
            #print(f"moved west from ({row_num, c}) to ({row_num, col_num})")
            grid[row_num][col_num] = "O"
            grid[row_num][c] = "."
            return
        elif char == '#':
            return

def move_next_marble_east(grid, row_num, col_num):

    for c in range(col_num - 1, -1, -1):
        char = grid[row_num][c]
        if char == "O":
            #print(f"moved east from ({row_num, c}) to ({row_num, col_num})")
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
    for row_num in range(len(grid) - 1, -1, -1):
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
    for col_num in range(len(grid[0]) -1, -1, -1):
        for row_num in range(len(grid)):
            if grid[row_num][col_num] == ".":
                move_next_marble_east(grid, row_num, col_num)

def get_hash(grid):
    hash = ""
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == "O":
                hash += f"({row_num}, {col_num}) "
    return hash

def spin(grid):
    grid_hash_before = get_hash(grid)
    if grid_hash_before in spin_cache:
        #print(f">>>>> CACHE HIT <<<<<")
        return spin_cache[grid_hash_before]
    
    #print("BEFORE SPIN>>>")
    #display_matrix(grid)
    roll_north(grid)
    #print("AFTER ROLL NORTH:")
    #display_matrix(grid)
    roll_west(grid)
    #print("AFTER ROLL WEST")
    #display_matrix(grid)
    roll_south(grid)
    #print("AFTER ROLL SOUTH")
    #display_matrix(grid)
    roll_east(grid)
    #print("AFTER ROLL EAST")
    #display_matrix(grid)
    
    result = get_total_load(grid)

    spin_cache[grid_hash_before] = (copy.deepcopy(grid), result)

    return (grid, result)

def is_repeating_sequence(all_results, repeating_sequence_start, repeating_sequence_length):
    #repeating sequence must repeat all the way to the end

    result = False
    s1 = repeating_sequence_start
    e1 = s1 + repeating_sequence_length
    sequence = all_results[s1:e1]
    s2 = e1
    e2 = s2 + repeating_sequence_length
    while e2 < len(all_results):
        if all_results[s2:e2] != sequence:
            return False
        else:
            result = True
            s2 = e2
            e2 = s2 + repeating_sequence_length

    return result

def find_repeating_sequence(all_results):

    for repeating_sequence_length in range(2, len(all_results)//2):
        for repeating_sequence_start in range(0, len(all_results)-repeating_sequence_length):
            if is_repeating_sequence(all_results, repeating_sequence_start, repeating_sequence_length):
                print(f"Found Repeating Sequence at {repeating_sequence_start} of length {repeating_sequence_length}")
                sequence = all_results[repeating_sequence_start:repeating_sequence_start +repeating_sequence_length]
                print(sequence)
                return repeating_sequence_start, repeating_sequence_length, sequence

    raise Exception("Couldn't find repeating sequence.")

def extrapolate_results(all_results, extrapolation_limit):
    repeating_sequence_start, repeating_sequence_length, sequence = find_repeating_sequence(all_results)
    index = (extrapolation_limit - repeating_sequence_start) % repeating_sequence_length - 1
    return sequence[index]

def execute(input_lines):
    
    print(input_lines)
    grid = [ list(line) for line in input_lines ]
    #print(grid)
    
    all_results = []
    for i in range(1000):
        (grid, result) = spin(grid)
        all_results.append(result)
        #print(f"ITERATION {i} result: {result}")

    result = extrapolate_results(all_results, 1000000000)
    print(result)
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

# TESTS for Repeating Sequence

assert is_repeating_sequence([1, 2, 3, 4, 2, 3, 4, 2, 3], 1, 3) == True
assert is_repeating_sequence([1, 2, 3, 4, 2, 3, 5, 2, 3], 1, 3) == False
assert find_repeating_sequence([1, 2, 3, 4, 2, 3, 4, 2, 3]) == (1, 3, [2, 3, 4])

print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 14

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 64
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 99291
print("ANSWER CORRECT")
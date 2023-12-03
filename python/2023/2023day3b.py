from utilities import *
import math
import copy
import numpy

def is_symbol(char):
    if char.isdigit():
        return False
    elif char == '.':
        return False
    else:
        return True

def is_adjacent_to_symbol(all_lines, row, col):
    adjacency = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]

    for (r, c) in adjacency:
        if row + r >= 0 and row + r < len(all_lines):
            if col + c >= 0 and col + c < len(all_lines[0]):
                if is_symbol(all_lines[row + r][col + c]):
                    return True
 
    return False

def get_neighbours(all_lines, row, col):
    adjacency = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]

    adjacent_parts = []
    visited = []

    for (r, c) in adjacency:
        if row + r >= 0 and row + r < len(all_lines):
            if col + c >= 0 and col + c < len(all_lines[0]):
                this_row = row + r
                this_col = col + c 
                if (this_row, this_col) not in visited:
                    visited.append((this_row, this_col))
                    char = all_lines[this_row][this_col]
                    if char.isdigit():

                        print(f'   Collecting part number from neighbour @ ({this_row}, {this_col})')

                        # we found a part number, now we need to collect the whole number
                        start_index = this_col
                        end_index = this_col

                        # LOOK LEFT
                        finished_collecting = False
                        while not finished_collecting:
                            left_index = start_index - 1
                            if left_index < 0: # we reached the beginning of the line
                                finished_collecting = True
                            elif not all_lines[this_row][left_index].isdigit(): # this part number is complete
                                finished_collecting = True
                            else:
                                start_index = left_index # digit starts to the left
                                visited.append((this_row, start_index))

                        # LOOK RIGHT
                        finished_collecting = False
                        while not finished_collecting:
                            right_index = end_index + 1
                            if right_index == len(all_lines[this_row]): # we reached the end of the line
                                finished_collecting = True
                            elif not all_lines[this_row][right_index].isdigit(): # this part number is complete
                                finished_collecting = True
                            else:
                                end_index = right_index # part number carried on to the right
                                visited.append((this_row, end_index))

                        part_number = all_lines[this_row][start_index:end_index+1]
                        print(f'   Found part number from neighbour @ ({this_row}, {this_col} => {part_number})')
                        adjacent_parts.append(int(part_number))

    return adjacent_parts

def execute(all_lines):
    print(all_lines)
    result = 0

    all_gears = []

    for row, line in enumerate(all_lines):
        for col, char in enumerate(line):
            if char == '*':
                print(f'GEAR @ ({row}, {col})')
                neighbours = get_neighbours(all_lines, row, col)
                if len(neighbours) == 2:
                    all_gears.append(numpy.prod(neighbours))
    
    result = numpy.sum(all_gears)
    print(f"result: {result}")
    return result

# TESTS
assert is_adjacent_to_symbol(["868*10"], 0, 2) == True
assert is_adjacent_to_symbol(["868*10"], 0, 4) == True
assert execute(["868*10"]) == 8680
print("ALL TESTS PASSED")

YEAR = 2023
DAY = 3

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 467835

# raw_input = get_input(YEAR, DAY, "_test2")
# input = get_strings(raw_input)
# assert execute(input) == 6288
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 84495585
print("ANSWER CORRECT")
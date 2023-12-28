from utilities import *
import math
import copy
import itertools

def parse_input(input_lines):

    galaxy_locations = []
    empty_rows = []

    for row_number, row in enumerate(input_lines):
        is_empty_row = True
        for col_number, char in enumerate(row):
            if char == '#':
                galaxy_locations.append((row_number, col_number))
                is_empty_row = False
        if is_empty_row:
            empty_rows.append(row_number)

    empty_columns = []
    for col_number in range(len(input_lines[0])):
        is_empty_col = True
        for row in input_lines:
            char = row[col_number]
            if char == '#':
                is_empty_col = False
        if is_empty_col:
            empty_columns.append(col_number)

    return galaxy_locations, empty_rows, empty_columns

def get_num_empty_between(start, end, empties):
    num_empty_between = 0
    for empty in empties:
        if empty > min(start, end) and empty < max(start, end):
            num_empty_between += 1
    return num_empty_between

def get_sum_of_shortest_paths(galaxy_locations, empty_rows, empty_columns):
    sum_of_shortest_paths = 0

    perms = list(itertools.combinations(galaxy_locations, 2))
    print(f"{len(perms)} combinations of galaxies")

    for ((g1_r, g1_c), (g2_r, g2_c)) in perms:

        num_empty_cols = get_num_empty_between(g1_c, g2_c, empty_columns)
        num_empty_rows = get_num_empty_between(g1_r, g2_r, empty_rows)

        shortest_path = abs(g1_r - g2_r) + num_empty_rows + abs(g1_c - g2_c) + num_empty_cols
        sum_of_shortest_paths += shortest_path

    return sum_of_shortest_paths

def execute(input_lines):
    print(input_lines)
    galaxy_locations, empty_rows, empty_columns = parse_input(input_lines)
    result = get_sum_of_shortest_paths(galaxy_locations, empty_rows, empty_columns)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 11

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 374
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 9445168
print("ANSWER CORRECT")
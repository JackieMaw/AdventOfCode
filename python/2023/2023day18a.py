from utilities import *
import math
import copy


def display_lean_matrix(matrix_positions):

    max_x = max([x for (x, y) in matrix_positions])
    min_x = min([x for (x, y) in matrix_positions])
    max_y = max([y for (x, y) in matrix_positions])
    min_y = min([y for (x, y) in matrix_positions])

    print('-'.join(['-' for _ in range(min_y, max_y + 1)]))
    for r in range(max_x, min_x - 1, -1):
        for c in range(min_y, max_y + 1):
            if (r, c) in matrix_positions:
                print('#', end ="")
            else:
                print('.', end ="")
        print("")

def parse_input(input_lines):
    return [input_line.split() for input_line in input_lines]



def get_area_of_trench(matrix_positions):

    max_x = max([x for (x, y) in matrix_positions])
    min_x = min([x for (x, y) in matrix_positions])

    return sum(get_area_of_trench_for_row(matrix_positions, r) for r in range(max_x, min_x - 1, -1))

# ray-casting algorithm
def get_area_of_trench_for_row(matrix_positions, r):

    matrix_positions_with_area = copy.deepcopy(matrix_positions)

    max_y = max([y for (x, y) in matrix_positions])
    min_y = min([y for (x, y) in matrix_positions])

    inside = False
    number_of_tiles_inside = 0

    for c in range(min_y, max_y + 1):
        if (r, c) in matrix_positions:
            inside = not inside
        else:            
            if inside:
                number_of_tiles_inside += 1
                matrix_positions_with_area.add((r, c))
       
    display_lean_matrix(matrix_positions_with_area)

    return number_of_tiles_inside

def solve(instructions):

    dugout = set()
    x, y = 0, 0
    for instruction in instructions:
        [direction, distance, paint] = instruction
        distance = int(distance)
        for _ in range(distance):
            if direction == "U":
                x += 1
            elif direction == "D":
                x -= 1
            elif direction == "R":
                y += 1
            elif direction == "L":
                y -= 1
            else:
                raise Exception(f"Unexpected case: {instruction}")
            dugout.add((x, y))

    display_lean_matrix(dugout)

    return get_area_of_trench(dugout)

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 18

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 62
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
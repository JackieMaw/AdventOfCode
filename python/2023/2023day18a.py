from utilities import *
import math
import copy


def display_lean_matrix(matrix_positions, matrix_positions_internal):

    max_x = max([x for (x, y) in matrix_positions])
    min_x = min([x for (x, y) in matrix_positions])
    max_y = max([y for (x, y) in matrix_positions])
    min_y = min([y for (x, y) in matrix_positions])

    print('-'.join(['-' for _ in range(min_y, max_y + 1)]))
    for r in range(max_x, min_x - 1, -1):
        for c in range(min_y, max_y + 1):
            if (r, c) in matrix_positions:
                print('#', end ="")
            elif (r, c) in matrix_positions_internal:
                print('I', end ="") 
            else:
                print('.', end ="")
        print("")

def parse_input(input_lines):
    return [input_line.split() for input_line in input_lines]

def get_area_of_trench(matrix_positions, matrix_positions_internal):

    max_x = max([x for (x, y) in matrix_positions])
    min_x = min([x for (x, y) in matrix_positions])

    for r in range(max_x, min_x - 1, -1):
        get_area_of_trench_for_row(matrix_positions, matrix_positions_internal,  r)

    return len(matrix_positions) + len(matrix_positions_internal)

# ray-casting algorithm
def get_area_of_trench_for_row(perimeter, internal, r):

    max_y = max([y for (x, y) in perimeter])
    min_y = min([y for (x, y) in perimeter])

    inside = False
    on_the_line = False
    left_corner = None

    for c in range(min_y, max_y + 1):
        if (r, c) in perimeter:
            if not on_the_line:
                inside = not inside
                on_the_line = True
                left_corner = None
                if (r-1, c) in perimeter:
                    left_corner = "UPPER"
                elif (r+1, c) in perimeter:
                    left_corner = "LOWER"
            else: # now we are really on the line!
                right_corner = None                
                if (r-1, c) in perimeter:
                    right_corner = "UPPER"
                elif (r+1, c) in perimeter:
                    right_corner = "LOWER"
                if right_corner is not None: # we are at the end of the line
                    if left_corner == right_corner:
                        inside = not inside
        else:        
            on_the_line = False
            if inside:
                internal.add((r, c))

def solve(instructions):

    permimeter = set()
    internal = set()
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
            permimeter.add((x, y))

    display_lean_matrix(permimeter, internal)

    area = get_area_of_trench(permimeter, internal)

    display_lean_matrix(permimeter, internal)

    return area

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
assert execute(input_lines) == 48400
print("ANSWER CORRECT")
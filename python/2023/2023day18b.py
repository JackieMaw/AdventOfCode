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

def decode_instruction(input_line):

    # R 6 (#70c710)
    [_, _, hex_code] = input_line.split()

    #five-digit hexadecimal number. 
    # The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.
    # 012345678
    # (#70c710) = R 461937 

    distance = int(hex_code[2:7], base=16)
    direction_code = hex_code[7]
    direction = None
    if direction_code == '0':
        direction = 'R'
    elif direction_code == '1':
        direction = 'D'
    elif direction_code == '2':
        direction = 'L'
    elif direction_code == '3':
        direction = 'U'

    return (direction, distance)

def parse_input(input_lines):
    return [decode_instruction(input_line) for input_line in input_lines]

def get_perimeter_of_trench(corners):

    perimeter = 0
    for i, this_corner in enumerate(corners):
        if i < len(corners) - 1:
            next_corner = corners[i + 1]
        else:
            next_corner = corners[0]
        perimeter += abs(this_corner[0] - next_corner[0]) + abs(this_corner[1] - next_corner[1])

    return perimeter

# shoelace algorithm
def get_area_of_trench(corners):

    sum1 = 0
    sum2 = 0
    for i, this_corner in enumerate(corners):
        if i < len(corners) - 1:
            next_corner = corners[i + 1]
        else:
            next_corner = corners[0]
        sum1 += this_corner[0] * next_corner[1]
        sum2 += this_corner[1] * next_corner[0]
    
    area = abs(sum1 - sum2)//2

    return area

def draw_polygon(instructions):

    corners = [(0,0)]
    x, y = 0, 0

    for instruction in instructions:
        (direction, distance) = instruction
        distance = int(distance)
        
        if direction == "U":
            x += distance
        elif direction == "D":
            x -= distance
        elif direction == "R":
            y += distance
        elif direction == "L":
            y -= distance
        else:
            raise Exception(f"Unexpected case: {instruction}")
        
        corners.append((x, y))

    #display_lean_matrix(permimeter, internal)

    area = get_area_of_trench(corners)
    perimeter = get_perimeter_of_trench(corners)
    result = int(area + perimeter * 0.5) + 1

    print(f"area: {area}")
    print(f"perimeter: {perimeter}")

    #display_lean_matrix(permimeter, internal)

    return result

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = draw_polygon(initial_state)
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
assert execute(input_lines) == 952408144115
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 72811019847283
print("ANSWER CORRECT")
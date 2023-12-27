import heapq
from itertools import count
import itertools
from utilities import *
import math
import copy

north = (-1, 0)
east = (0, +1)
south = (+1, 0)
west = (0, -1)

all_neighbour_offsets = [north, east, south, west]

neighbour_rules = {'|' : [north, south], #incoming vertical, outgoing vertical
              '-' : [east, west], #incoming horizontal, outgoing horizontal
              'L' : [north, east], #incoming vertical, outgoing horizontal
              'J' : [north, west], #incoming horizontal, incoming vertical
              '7' : [west, south], #incoming horizontal, outgoing vertical
              'F' : [east, south], #outgoing horizontal, outgoing vertical
              '.' : [],
              'S' : [north, east, south, west]}

compatability_rules = { north : ['|', '7', 'F'],
                       east : ['-', '7', 'J'],
                       south : ['|', 'J', 'L'],
                       west : ['-', 'L', 'F'],
                        }

def get_starting_position(input_lines):
    for line_number, input_line in enumerate(input_lines):
        col_number = input_line.find('S')
        if col_number >= 0:
            return (line_number, col_number)
    raise Exception("Could not find starting position")

num_rows = None
num_cols = None

def is_valid_location(location):
    (row, col) = location
    global num_rows
    global num_cols
    if row < 0 or col < 0 or row >= num_rows or col >= num_cols:
        return False
    return True

def get_starting_character(possible_neighbours):
    if north in possible_neighbours and south in possible_neighbours:
        return '|'
    if north in possible_neighbours and east in possible_neighbours:
        return 'J'
    if north in possible_neighbours and west in possible_neighbours:
        return 'J'
    
    if east in possible_neighbours and west in possible_neighbours:
        return '-'
    if east in possible_neighbours and south in possible_neighbours:
        return 'F'
    
    if south in possible_neighbours and west in possible_neighbours:
        return '7'
    
    raise Exception(f"Unexpected case for possible_neighbours of starting character: {possible_neighbours}")
    

def get_neighbours(current_location, grid):
    (row, col) = current_location
    char = grid[row][col]
    possible_neighbours = []
    neighbour_offsets = []

    for neighbour_offset in neighbour_rules[char]:
        (row_offset, col_offset) = neighbour_offset
        new_row = row + row_offset
        new_col = col + col_offset
        new_location = (new_row, new_col)
        if is_valid_location(new_location):
            new_char = grid[new_row][new_col]
            if new_char in compatability_rules[neighbour_offset]:
                possible_neighbours.append(new_location)
                neighbour_offsets.append(neighbour_offset)

    return possible_neighbours, neighbour_offsets

def display_matrix(matrix):
    print('-'.join(['-' for col in matrix[0]]))
    for row in matrix:
        print(' '.join([str(col) for col in row]))

# Djikstra's Algorithm - Shortest Path to All Nodes for Weighted Graph
# Actually this graph is not weighted, each edge has length one
# So it's just a breadth-first search
# In this case, priority queue is probably not necessary

def traverse_loop(grid, starting_position):

    global num_rows
    num_rows = len(grid)
    global num_cols
    num_cols = len(grid[0])

    simple_grid = [ [ 'X' for _ in range(num_cols) ] for _ in range(num_rows) ]
    distance_grid = [ [ 'X' for _ in range(num_cols) ] for _ in range(num_rows) ]
    already_visited = [ [ 0 for _ in range(num_cols) ] for _ in range(num_rows) ]

    (row_start, col_start) = starting_position
    nodes_to_visit_priority_queue = [(0, starting_position)] # (cost, (row, col))
    distance_grid[row_start][col_start] = 0
    already_visited[row_start][col_start] = 1
    simple_grid[row_start][col_start] = 'S'

    # display_matrix(grid)
    # display_matrix(simple_grid)
    # display_matrix(distance_grid)
    # display_matrix(already_visited)

    while len(nodes_to_visit_priority_queue) > 0:
        (distance_to_here, (row, col)) = heapq.heappop(nodes_to_visit_priority_queue)
        already_visited[row][col] = 1
        simple_grid[row][col] = grid[row][col]
        #print(f"Visiting: {(row, col)}")
        possible_neighbours, neighbour_offsets = get_neighbours((row, col), grid)
        
        if grid[row][col] == 'S':
            simple_grid[row][col] = get_starting_character(neighbour_offsets)

        neighbours = [possible_neighbour for possible_neighbour in possible_neighbours if possible_neighbour not in already_visited]

        for (nrow, ncol) in neighbours:
            #print(f"  >> {(nrow, ncol)}")
            distance_to_neighbour = distance_grid[nrow][ncol]
            new_distance_to_neighbour = distance_to_here + 1
            if distance_to_neighbour == 'X' or new_distance_to_neighbour < distance_to_neighbour:
                #print(f"    found shortest path to {(nrow, ncol)} : {new_distance_to_neighbour}")
                distance_grid[nrow][ncol] = new_distance_to_neighbour
                # do not add if already visited
                if not already_visited[nrow][ncol]:
                    heapq.heappush(nodes_to_visit_priority_queue, (new_distance_to_neighbour, (nrow, ncol)))


    # display_matrix(grid)
    # display_matrix(simple_grid)
    display_matrix(distance_grid)
    # display_matrix(already_visited)

    return simple_grid

def is_not_none(x):
    return x != 'X'


# ray-casting algorithm
def get_number_of_tiles_inside_loop(row):

    inside = False
    number_of_tiles_inside = 0

    previous_corner = None

    for col, char in enumerate(row):
        if char == 'X':
            if inside:
                number_of_tiles_inside += 1
                row[col] = 'I'
            else:
                row[col] = 'O'
        elif char == '-':
            pass
        elif char == '|':
            inside = not inside
        elif char in ['F','J','L','7']:
            if previous_corner is None:
                previous_corner = char
                inside = not inside
            else:
                if previous_corner == 'F':
                    if char == '7': # diff direction
                        inside = not inside
                        previous_corner = None
                    elif char == 'J': # same direction
                        #inside = inside
                        previous_corner = None
                    else:
                        raise Exception(f"Unexpected case for corner: {char}")
                elif previous_corner == 'L':
                    if char == '7': # same direction
                        #inside = inside
                        previous_corner = None
                    elif char == 'J': # diff direction
                        inside = not inside
                        previous_corner = None
                    else:
                        raise Exception(f"Unexpected case for corner: {char}")
                else:
                    raise Exception(f"Unexpected case for corner: {char} and previous_corner: {char} for row: {row}")
        else:
            raise Exception(f"Unexpected case: {char}")

    return number_of_tiles_inside

def get_total_number_of_dots_inside_loop(input_lines):
    starting_position = get_starting_position(input_lines)
    simple_grid = traverse_loop(input_lines, starting_position)
    display_matrix(simple_grid)
    print(simple_grid)
    result = sum(get_number_of_tiles_inside_loop(row) for row in simple_grid)
    display_matrix(simple_grid)
    
    return result

def execute(input_lines):
    #print(input_lines)
    result = get_total_number_of_dots_inside_loop(input_lines)
    print(f"result: {result}")
    return result

# UNIT TESTS
#[['X', 'X', 'F', '7', 'X'], ['X', 'F', 'J', '|', 'X'], ['S', 'J', 'X', 'L', '7'], ['|', 'F', '-', '-', 'J'], ['L', 'J', 'X', 'X', 'X']]

assert get_number_of_tiles_inside_loop(['X', 'X', 'F', '7', 'X']) == 0
assert get_number_of_tiles_inside_loop(['X', 'F', 'J', '|', 'X']) == 0
assert get_number_of_tiles_inside_loop(['F', 'J', 'X', 'L', '7']) == 1
assert get_number_of_tiles_inside_loop(['|', 'F', '-', '-', 'J']) == 0
assert get_number_of_tiles_inside_loop(['L', 'J', 'X', 'X', 'X']) == 0
print("ALL UNIT TESTS PASSED")

YEAR = 2023
DAY = 10

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 1
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 1
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 1
raw_input = get_input(YEAR, DAY, "_test4")
input = get_strings(raw_input)
assert execute(input) == 1
raw_input = get_input(YEAR, DAY, "_test5")
input = get_strings(raw_input)
assert execute(input) == 1
raw_input = get_input(YEAR, DAY, "_test6")
input = get_strings(raw_input)
assert execute(input) == 4
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 6897
print("ANSWER CORRECT")
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

neighbour_rules = {'|' : [north, south],
              '-' : [east, west],
              'L' : [north, east],
              'J' : [north, west],
              '7' : [west, south],
              'F' : [east, south],
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


def get_neighbours(current_location, grid, visited):    
    (row, col) = current_location
    char = grid[row][col]
    possible_neighbours = []
    for possible_neighbour in neighbour_rules[char]:
        (row_offset, col_offset) = possible_neighbour
        new_row = row + row_offset
        new_col = col + col_offset
        new_location = (new_row, new_col)
        if is_valid_location(new_location):
            new_char = grid[new_row][new_col]
            if new_char in compatability_rules[possible_neighbour]:
                possible_neighbours.append(new_location)
    
    not_visited_yet = [possible_neighbour for possible_neighbour in possible_neighbours if possible_neighbour not in visited]
    return not_visited_yet

def display_matrix(matrix):
    for row in matrix:
        print(' '.join([str(col) for col in row]))

#Djikstra's Algorithm - Shortest Path to All Nodes
def get_all_distances(grid, starting_position):

    global num_rows
    num_rows = len(grid)
    global num_cols
    num_cols = len(grid[0])

    distance_grid = [ [ 'X' for _ in range(num_cols) ] for _ in range(num_rows) ]
    already_visited = [ [ 0 for _ in range(num_cols) ] for _ in range(num_rows) ]

    (row_start, col_start) = starting_position
    nodes_to_visit_priority_queue = [(0, starting_position)] # (cost, (row, col))
    distance_grid[row_start][col_start] = 0
    already_visited[row_start][col_start] = 1

    display_matrix(grid)
    #display_matrix(distance_grid)
    #display_matrix(visited)

    while len(nodes_to_visit_priority_queue) > 0:
        (distance_to_here, (row, col)) = heapq.heappop(nodes_to_visit_priority_queue)
        already_visited[row][col] = 1
        print(f"Visiting: {(row, col)}")
        neighbours = get_neighbours((row, col), grid, already_visited)
        for (nrow, ncol) in neighbours:
            print(f"  >> {(nrow, ncol)}")
            distance_to_neighbour = distance_grid[nrow][ncol]
            new_distance_to_neighbour = distance_to_here + 1
            if distance_to_neighbour == 'X' or new_distance_to_neighbour < distance_to_neighbour:
                print(f"    found shortest path to {(nrow, ncol)} : {new_distance_to_neighbour}")
                distance_grid[nrow][ncol] = new_distance_to_neighbour
                # do not add if already visited
                if not already_visited[nrow][ncol]:
                    heapq.heappush(nodes_to_visit_priority_queue, (new_distance_to_neighbour, (nrow, ncol)))


    display_matrix(distance_grid)
    #display_matrix(visited)

    return distance_grid


def is_not_none(x):
    return x != 'X'

def get_max_distance(distance_grid):    
    all_distances = itertools.chain(*[list(filter(is_not_none, row)) for row in distance_grid])
    return max(all_distances)

def get_safest_distance_from_animal(input_lines):
    starting_position = get_starting_position(input_lines)
    distance_grid = get_all_distances(input_lines, starting_position)
    return get_max_distance(distance_grid)

def execute(input_lines):
    print(input_lines)
    result = get_safest_distance_from_animal(input_lines)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 10

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 4
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 4
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 8
raw_input = get_input(YEAR, DAY, "_test4")
input = get_strings(raw_input)
assert execute(input) == 8
raw_input = get_input(YEAR, DAY, "_test5")
input = get_strings(raw_input)
assert execute(input) == 5
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 6897
print("ANSWER CORRECT")
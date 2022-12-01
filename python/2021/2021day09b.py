#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

global x_max, y_max

def read_matrix(input):
    matrix = []
    for line in input:
        matrix.append(list(int(char) for char in line))   

    global x_max, y_max
    x_max = len(input)
    y_max = len(input[0])

    return matrix

def is_lowest(matrix, x, y):
    global x_max, y_max
    this_low = matrix[x][y]
    # Diagonal locations do not count as adjacent
    neighbours = [(-1, 0), (0, 1), (1,0), (0, -1)]
    for (dx, dy) in neighbours:
        x1 = x + dx
        y1 = y + dy
        if x1 >= 0 and x1 < x_max and y1 >= 0 and y1 < y_max:
            neighbour = matrix[x1][y1]   
            if neighbour <= this_low:
                return False  
    return True

def get_basin_size(matrix, x, y, visited):
    #count myself as visited, don't visit me again!
    visited.append((x, y))

    # recursive function, base case
    if matrix[x][y] == 9:
        #print(f"({x}, {y}) ====> {0}")
        return 0

    total_basin_size = 1
    #reduce problem space 
    neighbours = [(-1, 0), (0, 1), (1,0), (0, -1)]
    #neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for (dx, dy) in neighbours:
        x1 = x + dx
        y1 = y + dy
        if x1 >= 0 and x1 < x_max and y1 >= 0 and y1 < y_max:
            if (x1, y1) not in visited:
                #print(f"({x}, {y}) => visiting @ ({x1}, {y1})")
                total_basin_size += get_basin_size(matrix, x1, y1, visited)

    #print(f"({x}, {y}) ====> {total_basin_size}")
    return total_basin_size

def execute(input):
    print(input)

    matrix = read_matrix(input)

    basin_sizes = []
    visited = []
    global x_max, y_max
    for x in range(0, x_max):
        for y in range (0, y_max):
            if (is_lowest(matrix, x, y)):
                basin_size = get_basin_size(matrix, x, y, visited)
                print(f"basin_size @ ({x}, {y}) => {basin_size}")
                basin_sizes.append(basin_size)

    basin_sizes.sort(reverse=True)
    total_basin_measure = 1
    for basin_size in basin_sizes[:3]:
        total_basin_measure = total_basin_measure * basin_size

    result = total_basin_measure
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 9

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
matrix = read_matrix(input)
assert is_lowest(matrix, 0, 1) == True
assert get_basin_size(matrix, 0, 1, []) == 3
assert is_lowest(matrix, 0, 9) == True
assert get_basin_size(matrix, 0, 9, []) == 9
assert is_lowest(matrix, 2, 2) == True
assert get_basin_size(matrix, 2, 2, []) == 14
assert is_lowest(matrix, 4, 6) == True
assert get_basin_size(matrix, 4, 6, []) == 9
assert execute(input) == 1134
print("TEST INPUT PASSED")

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
matrix = read_matrix(input)
assert is_lowest(matrix, 0, 0) == True
assert is_lowest(matrix, 0, 1) == False
assert execute(input) == 1
print("TEST 2 INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 1048128
print("ANSWER CORRECT")
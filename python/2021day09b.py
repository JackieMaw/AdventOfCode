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

def execute(input):
    print(input)

    matrix = read_matrix(input)

    risk = 0
    global x_max, y_max
    for x in range(0, x_max):
        for y in range (0, y_max):
            if (is_lowest(matrix, x, y)):
                print(f"found low @ ({x}, {y})")
                risk += matrix[x][y] + 1

    result = risk
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
assert is_lowest(matrix, 0, 0) == False
assert is_lowest(matrix, 0, 1) == True
assert execute(input) == 15
print("TEST INPUT PASSED")

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
matrix = read_matrix(input)
assert is_lowest(matrix, 0, 0) == True
assert is_lowest(matrix, 0, 1) == False
assert execute(input) == 63
print("TEST 2 INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 494
print("ANSWER CORRECT")
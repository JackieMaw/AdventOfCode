#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

def read_matrix(input):
    matrix = [[int(char) for char in line] for line in input]
    return matrix

def play_step(matrix):

# First, the energy level of each octopus increases by 1.#

    flashed = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] += 1
            if matrix[i][j] == 10:
                flashed.append((i, j))

    #print(f"Flashed: {len(flashed)}")
    #print(matrix)
            
# Then, any octopus with an energy level greater than 9 flashes. 
# This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. 
# If this causes an octopus to have an energy level greater than 9, it also flashes. 
# This process continues as long as new octopuses keep having their energy level increased beyond 9. 
# (An octopus can only flash at most once per step.)

    reset = []

    while len(flashed) > 0:
        newly_flashed = []
        for (x, y) in flashed:
            for i in range(max(x-1, 0), min(x+2, len(matrix))):
                for j in range(max(y-1, 0), min(y+2, len(matrix[i]))):
                    if not (i == x and j == y):
                        #print(f"Increasing Energy for: ({i}, {j})")
                        matrix[i][j] += 1
                        if matrix[i][j] == 10:
                            newly_flashed.append((i, j))
            reset.append((x, y))
        flashed = newly_flashed      
        #print(f"Flashed: {len(flashed)}")
        #print(matrix)

# Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.

    for (x, y) in reset:
        matrix[x][y] = 0
    
    #print(matrix)

    return len(reset)


def execute(input, steps):
    print(input)

    matrix = read_matrix(input)
    total_num_flashed = 0
    for i in range(steps):
        num_flashed = play_step(matrix)
        print(f"{i} => num_flashed: {num_flashed}") 
        total_num_flashed += num_flashed

    result = total_num_flashed
    print(f"result: {result}") 
    return result

# TESTS
matrix = [[1,1,1], [1,9,1], [1,1,1]]
expected_matrix = [[3,3,3], [3,0,3], [3,3,3]]
assert play_step(matrix) == 1
expected_matrix = [[3,3,3], [3,0,3], [3,3,3]]
assert matrix == expected_matrix
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 11

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input, 1) == 9
assert execute(input, 2) == 9
print("TEST INPUT PASSED")

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input, 100) == 1656
print("TEST 2 INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input, 100) == 1599
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from typing import no_type_check
from utilities import *
import math
import copy

def get_num_overlapping_lines(grid):
    total_count = sum([numLines for numLines in grid.values()])
    print(f"total_count: {total_count}") 

    overlapping = len([numLines for numLines in grid.values() if numLines > 1])
    print(f"overlapping: {overlapping}") 
    return overlapping

def add_to_grid(x, y, grid):
    if (x, y) in grid:
        grid[x, y] += 1
    else:
        grid[x, y] = 1

def process_line(line, grid):
    # "937,275 -> 937,38"
    points = line.split(" -> ")
    pt1 = points[0].split(",")
    pt2 = points[1].split(",")

    xChange = int(pt2[0]) - int(pt1[0])
    xMove = 0
    if xChange > 1:
        xMove = 1
    elif xChange < 0:
        xMove = -1       

    yChange = int(pt2[1]) - int(pt1[1])
    yMove = 0
    if yChange > 1:
        yMove = 1
    elif yChange < 0:
        yMove = -1    
        
    if xChange == 0 and yChange == 0:
        print(f"Edge case found - line has length 0: {line}")

    if xChange != 0 and yChange != 0:
        # ignore diagonals
        return 0

    magnitude = max(xChange * xMove, yChange * yMove)

    num_marked = 0
    x = int(pt1[0])
    y = int(pt1[1])
    add_to_grid(x, y, grid)
    num_marked += 1
    for i in range(magnitude):
        x += xMove                 
        y += yMove
        add_to_grid(x, y, grid)
        num_marked += 1
    
    assert num_marked == magnitude + 1

    return num_marked

def execute(input):
    
    grid = { }  

    for line in input:
        num_marked = process_line(line, grid)
        print(f"num_marked: {num_marked} [{line}]") 

    result = get_num_overlapping_lines(grid)
    print(f"result: {result}") 
    return result

YEAR = 2021
DAY = 5

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 5
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 5774
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

#grid[(0, 0)] = "*" CENTRAL PORT
#grid[(p.x, p.y)] = "X" INTERSECTION
#grid[(p.x, p.y)] = "0" WIRE 0

def transform(point, fold_line):
    (x, y) = point
    (xfold, yfold) = fold_line
    if xfold is not None:
        if x > xfold:
            x = xfold - (x - xfold)
    if yfold is not None:
        if y > yfold:
            y = yfold - (y - yfold)
    return (x, y)

def print_grid(grid):
    max_x = max([x for (x, y) in grid])
    max_y = max([y for (x, y) in grid])

    print(f"grid:") 
    for y in range(max_y + 1):
        print_line = ""
        for x in range(max_x + 1):
            print_line += "#" if (x, y) in grid else "."
        print(print_line)

def process_input(input):
    grid = set() # grid{(x, y)}
    fold = [] # fold[("y", 7), ("x", 5)]

    processMoreDots = True
    for line in input:
        if line == "":
            processMoreDots = False
        elif processMoreDots:
            line_parts = line.split(",")
            grid.add((int(line_parts[0]), int(line_parts[1])))
        else:
            # fold along x=655
            line = line.replace("fold along ", "")
            line_parts = line.split("=")
            if line_parts[0] == "x":
                fold.append((int(line_parts[1]), None))
            elif line_parts[0] == "y":
                fold.append((None, int(line_parts[1])))                
    
    return grid, fold

def apply_fold(grid, fold_line):    

    print(f"apply_fold: {fold_line}") 
    for dot in grid.copy():
        new_dot = transform(dot, fold_line)
        if new_dot != dot:
            grid.remove(dot)
            grid.add(new_dot)

def count_dots(grid):
    return len(grid)

def execute(input):
    print(input)

    grid, fold = process_input(input)

    print_grid(grid)
    print(f"fold: {fold}") 

    for fold_line in fold:
        apply_fold(grid, fold_line)
        print_grid(grid)

    result = count_dots(grid)
    print(f"result: {result}") 
    return result

# TESTS
assert transform((8, 8), (None, 7)) == (8, 6)
assert transform((8, 6), (None, 7)) == (8, 6)
assert transform((8, 8), (7, None)) == (6, 8)
assert transform((6, 8), (7, None)) == (6, 8)
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 13

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 16
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 98
print("ANSWER CORRECT")

# LGHEGUEJ
#.....##..#..#.####..##..#..#.####...##
#....#..#.#..#.#....#..#.#..#.#.......#
#....#....####.###..#....#..#.###.....#
#....#.##.#..#.#....#.##.#..#.#.......#
#....#..#.#..#.#....#..#.#..#.#....#..#
####..###.#..#.####..###..##..####..##.
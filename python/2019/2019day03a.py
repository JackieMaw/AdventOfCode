#TODO - how to share utilities?
from utilities import *
import math
import copy

def execute(input):
    #init the grid, empty dictionary
    grid = { }
    x = 0
    y = 0  
    grid[(x, y)] = "O"    
    shortest_distance = None
    #print_grid(grid)
    #process the wire
    for wire_number, wire in enumerate(input):
        x = 0
        y = 0  
        for segment in wire:
            #print(segment)
            direction = segment[0]
            magnitude = int(segment[1])
            if direction == "R":
                for i in range(magnitude):
                    y += 1
                    if ((x, y) in grid):
                        grid[(x, y)] = "X"
                        distance = x + y
                        print(f"Wires Crossed at: {x} {x}, distance = {distance}")
                        if shortest_distance is None or distance < shortest_distance:
                            shortest_distance = distance
                    else:
                        grid[(x, y)] = str(wire_number)
            if direction == "U":
                for i in range(magnitude):
                    x += 1
                    if ((x, y) in grid):
                        grid[(x, y)] = "X"
                        distance = x + y
                        print(f"Wires Crossed at: {x} {x}, distance = {distance}")
                        if shortest_distance is None or distance < shortest_distance:
                            shortest_distance = distance
                    else:
                        grid[(x, y)] = str(wire_number)
            if direction == "L":
                for i in range(magnitude):
                    y -= 1
                    if ((x, y) in grid):
                        grid[(x, y)] = "X"
                        distance = x + y
                        print(f"Wires Crossed at: {x} {x}, distance = {distance}")
                        if shortest_distance is None or distance < shortest_distance:
                            shortest_distance = distance
                    else:
                        grid[(x, y)] = str(wire_number)
            if direction == "D":
                for i in range(magnitude):
                    x -= 1
                    if ((x, y) in grid):
                        grid[(x, y)] = "X"
                        distance = x + y
                        print(f"Wires Crossed at: {x} {x}, distance = {distance}")
                        if shortest_distance is None or distance < shortest_distance:
                            shortest_distance = distance
                    else:
                        grid[(x, y)] = str(wire_number)
            #print_grid(grid)
    # where are the wires crossed
    return shortest_distance

# def print_grid(grid):
#     for row in range(len(grid)):
#         row_string = ""
#         for col in range(len(grid[row])):
#             row_string += grid[row][col]
#         print(row_string)

# def get_closest_intersection(grid):
#     shortest_distance = 100
#     for row in range(len(grid)):
#         for col in range(len(grid[row])):
#             if grid[row][col] == "X":
#                 distance = (len(grid) - 1 - row) + (col - 0)
#                 print(f"Wires Crossed at: {row} {col}, distance = {distance}")
#                 if distance < shortest_distance:
#                     shortest_distance = distance
#     return shortest_distance

assert execute(get_strings_csv(["R8,U5,L5,D3","U7,R6,D4,L4"])) == 6
assert execute(get_strings_csv(["R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83"])) == 159
assert execute(get_strings_csv(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])) == 135
print("ALL TESTS PASSED")

# YEAR = 2019
# DAY = 3
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings_csv(raw_input)
# assert execute(input) == 9342
# print("ANSWER CORRECT")
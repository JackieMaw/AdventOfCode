#TODO - how to share utilities?
from utilities.utilities import *
import math
import copy

#grid[(0, 0)] = "*" CENTRAL PORT
#grid[(p.x, p.y)] = "X" INTERSECTION
#grid[(p.x, p.y)] = "0" WIRE 0
grid = { }
shortest_distance = None

#p = position(0, 0) current position
class position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

def execute(input):
    #init the grid, empty dictionary
    global grid
    grid = { }
    global shortest_distance
    shortest_distance = None
    p = position(0, 0)
    grid[(p.x, p.y)] = "*"    
    #print_grid(grid)
    #process the wire
    for wire_number, wire_segments in enumerate(input):
        p.x = 0
        p.y = 0  
        wire = str(wire_number)
        print(f"Wire {wire} starting at ({p.x}, {p.y})")
        for segment in wire_segments:
            #print(segment)
            process_wire_segment(segment, p, wire)
            print(f"+ {segment} => ({p.x}, {p.y})")
    #print_grid(grid)
    # where are the wires crossed
    return shortest_distance

def process_wire_segment(segment, p, wire):
    direction = segment[0]
    magnitude = int(segment[1:])
    if direction == "R":
        for i in range(magnitude):
            p.y += 1
            set_wire_at(p, wire)                    
    if direction == "U":
        for i in range(magnitude):
            p.x += 1
            set_wire_at(p, wire) 
    if direction == "L":
        for i in range(magnitude):
            p.y -= 1
            set_wire_at(p, wire) 
    if direction == "D":
        for i in range(magnitude):
            p.x -= 1
            set_wire_at(p, wire)   

def set_wire_at(p : position, wire):
    if grid.get((p.x, p.y), wire) != wire:
        grid[(p.x, p.y)] = "X"
        distance = abs(p.x) + abs(p.y)
        print(f"Wires Crossed at: {p.x} {p.y}, distance = {distance}")
        global shortest_distance
        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
    else:
        grid[(p.x, p.y)] = wire        

def get_max_range(grid):
    max_x = 0
    max_y = 0
    for (x, y) in grid.keys():
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    print(f"Max Range: ({max_x}, {max_y})")
    return (max_x, max_y)

def print_grid(grid):
    (max_x, max_y) = get_max_range(grid)
    for row in reversed(range(max_x)):
        row_string = ""
        for col in range(max_y):
            if (row, col) in grid:
                row_string += grid[(row, col)]
            else:
                row_string += "."
        print(row_string)

assert execute(get_strings_csv(["R8,U5,L5,D3","U7,R6,D4,L4"])) == 6
assert execute(get_strings_csv(["R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83"])) == 159
assert execute(get_strings_csv(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])) == 135
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 3
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings_csv(raw_input)
assert execute(input) == 627
print("ANSWER CORRECT")
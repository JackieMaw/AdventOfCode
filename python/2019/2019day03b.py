#TODO - how to share utilities?
from os import execl
from utilities.utilities import *
import math
import copy


#grid[(0, 0)] = [ { "0" : {0, 5, 9} }, {"1" : {0, 3, 6} }]

# p = position(0, 0) current position (need a class to pass by reference)
# is there a better way to do this?
class position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

grid = { }
current_position = position(0, 0)

def execute(input):

    #init the grid, empty dictionary
    global grid
    grid = { }  
    #print_grid(grid)
    
    #process the wire
    for wire_number, wire_segments in enumerate(input):
        global current_position
        current_position.x = 0
        current_position.y = 0 
        length = 0
        wire = str(wire_number)

        add_to_grid(wire, length)
        
        print(f"Wire {wire} starting at ({current_position.x}, {current_position.y})")
        for segment in wire_segments:
            #print(segment)
            length = process_wire_segment(segment, wire, length)
            print(f"+ {segment} => ({current_position.x}, {current_position.y})")
    #print_grid(grid)
    # where are the wires crossed
    return get_shortest_intersection()

def get_shortest_intersection():
    #print(grid)
    shortest_intersection = None
    # loop through each point in the grid
    # if any point has more than 1 wire then this is an intersection
    # ignore (0,0)
    # sum the first length for each wire
    # find the minimum of these
    for ((x, y), visit_logs) in grid.items():
        
        if x == 0 and y == 0:
            continue

        assert len(visit_logs) <= 2 # can we ever have a threesome? 

        if len(visit_logs) == 2:
            distance = 0
            for visit_log_for_wire in visit_logs.values():
                distance += visit_log_for_wire[0]
            print(f"Wires Crossed at: ({x}, {y}), distance = {distance}")
            if shortest_intersection is None or distance < shortest_intersection:
                shortest_intersection = distance 
    
    return shortest_intersection

def add_to_grid(wire, length):
    if (current_position.x, current_position.y) in grid:
        visit_logs = grid[(current_position.x, current_position.y)]
        if wire in visit_logs:
            visit_log_for_wire = visit_logs[wire]
            visit_log_for_wire.append(length)
        else:
            visit_log_for_wire = [ length ]
            visit_logs[wire] = visit_log_for_wire
    else:
        visit_log_for_wire = [ length ] # [] is a list
        visit_logs =  { wire: visit_log_for_wire } # {} is a dictionary (or set)
        grid[(current_position.x, current_position.y)] = visit_logs
    #print(grid)

def process_wire_segment(segment, wire, length):
    direction = segment[0]
    magnitude = int(segment[1:])
    if direction == "R":
        for i in range(magnitude):
            length += 1                 
            current_position.y += 1
            add_to_grid(wire, length)   
    if direction == "U":
        for i in range(magnitude):
            length += 1                 
            current_position.x += 1
            add_to_grid(wire, length)  
    if direction == "L":
        for i in range(magnitude):
            length += 1                 
            current_position.y -= 1
            add_to_grid(wire, length) 
    if direction == "D":
        for i in range(magnitude):
            length += 1                 
            current_position.x -= 1
            add_to_grid(wire, length) 
    return length  

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

assert execute(get_strings_csv(["R8,U5,L5,D3","U7,R6,D4,L4"])) == 30
assert execute(get_strings_csv(["R75,D30,R83,U83,L12,D49,R71,U7,L72","U62,R66,U55,R34,D71,R55,D58,R83"])) == 610
assert execute(get_strings_csv(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51","U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])) == 410
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 3
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings_csv(raw_input)
assert execute(input) == 13190
print("ANSWER CORRECT")
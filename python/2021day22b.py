#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def in_range(x, x_min, x_max):
    return x > x_min and x < x_max

class Point(object):
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z   

    def __str__(self):
        return f'({self.X}, {self.Y}, {self.Z})'

    def __repr__(self):
        return f'({self.X}, {self.Y}, {self.Z})'

class Cube(object):
    def __init__(self, start : Point, end : Point):
        self.Start = start
        self.End = end   

    def __str__(self):
        return f'[{self.Start} => {self.End}]'

    def __repr__(self):
        return f'[{self.Start} => {self.End}]'

    # def __init__(self, x_range, y_range, z_range):
    #     self.Start = Point(x_range[0], y_range[0], z_range[0])
    #     self.End = Point(x_range[1], y_range[1], z_range[1])  

    def is_contained_within(self, outer_cube):
        if self.Start.X < outer_cube.Start.X:
            return False
        if self.Start.Y < outer_cube.Start.Y:
            return False
        if self.Start.Z < outer_cube.Start.Z:
            return False
        if self.End.X > outer_cube.End.X:
            return False
        if self.End.Y > outer_cube.End.Y:
            return False
        if self.End.Z > outer_cube.End.Z:
            return False

        #print(f"Existing cube {self} is contained within {outer_cube}")
        return True

    
    def overlaps_with(self, other_cube):

        x_in_range = in_range(self.Start.X, other_cube.Start.X, other_cube.End.X) or in_range(self.End.X, other_cube.Start.X, other_cube.End.X)
        y_in_range = in_range(self.Start.Y, other_cube.Start.Y, other_cube.End.Y) or in_range(self.End.Y, other_cube.Start.Y, other_cube.End.Y)
        z_in_range = in_range(self.Start.Z, other_cube.Start.Z, other_cube.End.Z) or in_range(self.End.Z, other_cube.Start.Z, other_cube.End.Z)        

        result = x_in_range and y_in_range and z_in_range

        #if result:
        #    print(f"Existing cube {self} overlaps with {other_cube}")

        return result

    def size(self):
        return (self.End.X - self.Start.X) * (self.End.Y - self.Start.Y) * (self.End.Z - self.Start.Z)
    
    def is_valid(self):
        if self.Start.X >= self.End.X:
            return False
        if self.Start.Y >= self.End.Y:
            return False
        if self.Start.Z >= self.End.Z:
            return False
        return True

def get_segments(values):
    values.sort()
    segments = []
    for i in range(len(values) - 1):
        segments.append((values[i], values[i+1]))
    return segments

def split_cube_without_new_cube(existing_cube, new_cube):

    # we want to split the old cube into chunks and remove the chunk/s which are contained within the new cube

    split_cubes = []

    x_segments = get_segments([existing_cube.Start.X, existing_cube.End.X, new_cube.Start.X, new_cube.End.X])
    y_segments = get_segments([existing_cube.Start.Y, existing_cube.End.Y, new_cube.Start.Y, new_cube.End.Y])
    z_segments = get_segments([existing_cube.Start.Z, existing_cube.End.Z, new_cube.Start.Z, new_cube.End.Z])

    for x_segment in x_segments:
        for y_segment in y_segments:
            for z_segment in z_segments:
                start = Point(x_segment[0], y_segment[0], z_segment[0])
                end = Point(x_segment[1], y_segment[1], z_segment[1]) 
                split_cubes.append(Cube(start, end))

    existing_cube_split_without_new_cube = []

    for split_cube in split_cubes:
        # get rid of any cubes which have 0 size
        # the mini-cube must be part of the old cube
        # the mini-cube must NOT be part of the new cube        
        if split_cube.is_valid() and not split_cube.is_contained_within(new_cube) and split_cube.is_contained_within(existing_cube):
            existing_cube_split_without_new_cube.append(split_cube)

        # if not split_cube.is_valid():
        #     print(f"Mini-Cube rejected, NOT VALID: {split_cube}")
        # elif split_cube.is_contained_within(new_cube):
        #     print(f"Mini-Cube rejected, INSIDE NEW CUBE: {split_cube}")
        # elif not split_cube.is_contained_within(existing_cube):
        #     print(f"Mini-Cube rejected, OUTSIDE OLD CUBE: {split_cube}")                
        # else:
        #     print(f"Mini-Cube accepted: {split_cube}")       
        #     existing_cube_split_without_new_cube.append(split_cube)

    return existing_cube_split_without_new_cube

def get_range(string, limit):    
    line_parts = string.split("..")
    start = int(line_parts[0][2:])
    end = int(line_parts[1]) + 1
    if limit is not None:
        start = max(start, -limit)
        end = min(end, limit)
    return (start, end)

#on x=-20..26,y=-36..17,z=-47..7
def initialize(space, line, limit):

    switch_on = line[:2] == "on"

    line_parts = line.split(" ")[1].split(",")
    x_range = get_range(line_parts[0], limit)
    y_range = get_range(line_parts[1], limit)
    z_range = get_range(line_parts[2], limit)

    start = Point(x_range[0], y_range[0], z_range[0])
    end = Point(x_range[1], y_range[1], z_range[1])
    new_cube = Cube(start, end)

    # if this is not a valid cube within the limited space, ignore it
    if not new_cube.is_valid():
        return

    # if this is the first cube, just add it
    if len(space) == 0 and switch_on:
        space.add(new_cube)
        return

    cubes_to_remove = set()
    cubes_to_add = set()
    for existing_cube in space:
        if switch_on:
            if new_cube.is_contained_within(existing_cube):
                # new cube is a duplicate of an existing cube, we can ignore it completely
                return
            elif existing_cube.is_contained_within(new_cube):
                # new cube is larger than an existing cube, an existing cube can be removed
                cubes_to_remove.add(existing_cube)
            elif new_cube.overlaps_with(existing_cube):                   
                # new cube overlaps with an existing cube, the existing cube must be split and overlapping bits removed
                existing_cube_split_without_new_cube = split_cube_without_new_cube(existing_cube, new_cube)
                cubes_to_remove.add(existing_cube)
                for existing_cube_split in existing_cube_split_without_new_cube:
                    cubes_to_add.add(existing_cube_split)
        else: # switch off, just don't add the new cube
            if existing_cube.is_contained_within(new_cube):
                cubes_to_remove.add(existing_cube)                
            elif new_cube.overlaps_with(existing_cube):
                existing_cube_split_without_new_cube = split_cube_without_new_cube(existing_cube, new_cube)
                cubes_to_remove.add(existing_cube)
                for existing_cube_split in existing_cube_split_without_new_cube:
                    cubes_to_add.add(existing_cube_split)

    for cube_to_remove in cubes_to_remove:
        space.remove(cube_to_remove)

    for cube_to_add in cubes_to_add:
        space.add(cube_to_add)

    # we always add the new cube
    if switch_on:
        space.add(new_cube)

def execute(input, limit = None):
    #print(input)

    space = set()
    for line in input:
        initialize(space, line, limit)

    size = sum([cube.size() for cube in space])

    result = size
    print(f"result: {result}") 
    return result

# TESTS

# a single cube, 3x3
raw_input = ["on x=1..3,y=1..3,z=1..3"]
input = get_strings(raw_input)
assert execute(input) == 27

# two 3x3 cubes which do not overlap
raw_input = ["on x=1..3,y=1..3,z=1..3", "on x=4..6,y=4..6,z=4..6"]
input = get_strings(raw_input)
assert execute(input) == 54

# two identical 3x3 cubes
raw_input = ["on x=1..3,y=1..3,z=1..3", "on x=1..3,y=1..3,z=1..3"]
input = get_strings(raw_input)
assert execute(input) == 27

# second 2x2 cube is completely inside the first 3x3 cube
raw_input = ["on x=1..3,y=1..3,z=1..3", "on x=1..2,y=1..2,z=1..2"]
input = get_strings(raw_input)
assert execute(input) == 27

# second 2x2 cube is completely inside the first 3x3 cube
raw_input = ["on x=1..3,y=1..3,z=1..3", "on x=2..3,y=2..3,z=2..3"]
input = get_strings(raw_input)
assert execute(input) == 27

# first 2x2 cube is inside the second 3x3 cube
raw_input = ["on x=1..2,y=1..2,z=1..2", "on x=1..3,y=1..3,z=1..3"]
input = get_strings(raw_input)
assert execute(input) == 27

# first 2x2 cube is inside the second 3x3 cube
raw_input = ["on x=2..3,y=2..3,z=2..3", "on x=1..3,y=1..3,z=1..3"]
input = get_strings(raw_input)
assert execute(input) == 27

# two 3x3 cubes which overlap by 8
raw_input = ["on x=1..3,y=1..3,z=1..3", "on x=2..4,y=2..4,z=2..4"]
input = get_strings(raw_input)
assert execute(input) == 27 + 27 - 8

# two 3x3 cubes which overlap by 8 - the second one switches 8 blocks off
raw_input = ["on x=1..3,y=1..3,z=1..3", "off x=2..4,y=2..4,z=2..4"]
input = get_strings(raw_input)
assert execute(input) == 27 - 8

# two identical 3x3 cubes - the second one switches the first one off completely
raw_input = ["on x=1..3,y=1..3,z=1..3", "off x=1..3,y=1..3,z=1..3"]
input = get_strings(raw_input)
assert execute(input) == 0

YEAR = 2021
DAY = 22

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input, 50) == 39

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input, 50) == 590784

raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input, 50) == 474140 
assert execute(input) == 2758514936282235 # not 6726338736433640
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0 # not 2130779000262977
print("ANSWER CORRECT")
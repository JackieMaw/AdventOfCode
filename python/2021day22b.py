#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def in_range(x, x_min, x_max):
    return x >= x_min and x <= x_max

class Point(object):
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = y   

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

        print(f"Existing cube {self} is contained within {outer_cube}")
        return True

    
    def overlaps_with(self, other_cube):

        x_in_range = in_range(self.Start.X, other_cube.Start.X, other_cube.End.X) or in_range(self.End.X, other_cube.Start.X, other_cube.End.X)
        y_in_range = in_range(self.Start.Y, other_cube.Start.Y, other_cube.End.Y) or in_range(self.End.Y, other_cube.Start.Y, other_cube.End.Y)
        z_in_range = in_range(self.Start.Z, other_cube.Start.Z, other_cube.End.Z) or in_range(self.End.Z, other_cube.Start.Z, other_cube.End.Z)        

        return x_in_range and y_in_range and z_in_range

    def size(self):
        return (self.End.X - self.Start.X) * (self.End.Y - self.Start.Y) * (self.End.Z - self.Start.Z)
    
    def is_valid(self):
        if self.Start.X > self.End.X:
            return False
        if self.Start.Y > self.End.Y:
            return False
        if self.Start.Z > self.End.Z:
            return False
        return True

def split_cube_without_new_cube(old, new):

    bottom_slice = Cube(old.Start, Point(new.Start.X, old.End.Y, old.End.Z)) # same start point but the top is the bottom of the new cube
    top_slice = Cube(Point(new.End.X, old.Start.Y, old.Start.Z), old.End) # same end point but the bottom is the top of the new cube

    TODO, max and min the boundary points

    middle_cubes = { 
        # same X as the new cube, old.Start.Z => new.Start.Z
        Cube(Point(new.Start.X, old.Start.Y, old.Start.Z), Point(new.End.X, new.Start.Y, new.Start.Z)), 
        Cube(Point(new.Start.X, new.Start.Y, old.Start.Z), Point(new.End.X, new.End.Y, new.Start.Z)), 
        Cube(Point(new.Start.X, new.End.Y, old.Start.Z), Point(new.End.X, old.End.Y, new.Start.Z)),

        # same X as the new cube, new.Start.Z => new.End.Z
        Cube(Point(new.Start.X, old.Start.Y, new.Start.Z), Point(new.End.X, new.Start.Y, new.End.Z)), 
        #Cube(Point(new.Start.X, new.Start.Y, new.Start.Z), Point(new.End.X, new.End.Y, new.End.Z)), 
        Cube(Point(new.Start.X, new.End.Y, new.Start.Z), Point(new.End.X, old.End.Y, new.End.Z)),
        
        # same X as the new cube, new.End.Z => old.End.Z
        Cube(Point(new.Start.X, old.Start.Y, new.End.Z), Point(new.End.X, new.Start.Y, old.End.Z)), 
        Cube(Point(new.Start.X, new.Start.Y, new.End.Z), Point(new.End.X, new.End.Y, old.End.Z)), 
        Cube(Point(new.Start.X, new.End.Y,new.End.Z), Point(new.End.X, old.End.Y, old.End.Z)),
    }

    existing_cube_split_without_new_cube = set()
    if bottom_slice.is_valid():
        existing_cube_split_without_new_cube.add(bottom_slice)
    if top_slice.is_valid():
        existing_cube_split_without_new_cube.add(top_slice)
    for middle_cube in middle_cubes:
        if middle_cube.is_valid():
            existing_cube_split_without_new_cube.add(middle_cube)

    return existing_cube_split_without_new_cube


def get_range(string):    
    line_parts = string.split("..")
    start = int(line_parts[0][2:])
    end = int(line_parts[1])
    return (start, end)

#on x=-20..26,y=-36..17,z=-47..7
def initialize(space, line):

    switch_on = line[:2] == "on"

    line_parts = line.split(" ")[1].split(",")
    x_range = get_range(line_parts[0])
    y_range = get_range(line_parts[1])
    z_range = get_range(line_parts[2])

    start = Point(x_range[0], y_range[0], z_range[0])
    end = Point(x_range[1], y_range[1], z_range[1])
    new_cube = Cube(start, end)

    cubes_to_remove = set()
    cubes_to_add = set()
    for existing_cube in space:
        if switch_on:
            if existing_cube.is_contained_within(new_cube):
                cubes_to_remove.add(existing_cube)
            elif not new_cube.is_contained_within(existing_cube) and new_cube.overlaps_with(existing_cube):
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

    if switch_on:
        space.add(new_cube)

def execute(input):
    print(input)

    space = set()
    for line in input:
        initialize(space, line)

    size = sum([cube.size() for cube in space])

    result = size
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 22

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 39

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 590784

raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 2758514936282235
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 647076
print("ANSWER CORRECT")
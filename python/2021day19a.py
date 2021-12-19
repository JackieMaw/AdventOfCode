#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

class Scanner():
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

def add_to_space(tile, offset, space):
    for beacon in tile:
        (x, y) = beacon
        (ox, oy) = offset
        beacon_in_space = (x + ox, y + oy)
        space.append(beacon_in_space)

def parse_input(input):

    tiles = []

    current_tile = []
    for line in input:
        if line[:3] == "---": # ignore the first line
            continue
        if line == "": # this scanner is completed
            tiles.append(current_tile)
            current_tile = []
        else:
            line_parts = line.split(",")
            current_tile.append(int(line_parts[0]), line_parts[1])

    # this scanner is completed
    tiles.append(current_tile)

    return tiles

def rotate(tile):

    # tile: [ (x, y), (x, y) ]

    xs = [ x for (x, y) in tile] 
    x_min = min(xs)
    x_max = max(xs)
    
    ys = [ y for (x, y) in tile] 
    y_min = min(ys)
    y_max = max(ys)

    new_tile = []

    for (x, y) in tile:
        if (x >= 0 and y >= 0):
            new_beacon = (y, -x)
        elif (x >= 0 and y < 0):
            new_beacon = (y, -x)
        elif (x < 0 and y < 0):
            new_beacon = (y, -x)
        elif (x < 0 and y >= 0):
            new_beacon = (y, -x)
        new_tile.append(new_beacon)

    return new_tile

def get_all_rotations(tile):

    all_rotations = [tile]

    for _ in range(3):
        tile = rotate(tile)
        all_rotations.append(tile)

    #flipped = get_flipped(tile)
    return all_rotations


def get_bounds(tile):
    xs = [ x for (x, y) in tile] 
    x_min = min(xs)
    x_max = max(xs)
    
    ys = [ y for (x, y) in tile] 
    y_min = min(ys)
    y_max = max(ys)

    return ((x_min, x_max), (y_min, y_max)) 

def overlap(space, tile, offset):
    return True

def check_overlap(space, tile):

    space_bounds = get_bounds(space)
    ((space_x_min, space_x_max), (space_y_min, space_y_max)) = space_bounds
    tile_bounds = get_bounds(tile)
    ((tile_x_min, tile_x_max), (tile_y_min, tile_y_max)) = tile_bounds

    start_ox = 0 - space_x_min - tile_x_max
    end_ox = space_x_max - tile_x_min 
    start_oy = 0 - space_y_min - tile_y_max
    end_oy = space_y_max - tile_y_min 

    for ox in range(start_ox, end_ox):
        for oy in range (start_oy, end_oy):
            offset = (ox, oy)
            if overlap(space, tile, offset):
                return offset

    return None

def execute(input):
    print(input)

    tiles = parse_input(input) 

    space = set()
    
    # anchor the first tile
    next_tile = tiles.pop()
    add_to_space(next_tile, (0, 0), space)

    # for all remaining tiles, try to fit them into the existing space
    while len(tiles) > 0:
        next_tile = tiles.pop()
        tile_rotations = get_all_rotations(next_tile)
        for next_tile_rotation in tile_rotations:
            offset = check_overlap(space, next_tile_rotation)
            if offset is not None:
                add_to_space(next_tile, offset, space)
                break

    # count the number of beacons in space
    result = len(space)
    print(f"result: {result}") 
    return result

# TESTS
assert rotate([(1, 5)]) == [(5, -1)]
assert rotate([(5, -1)]) == [(-1, -5)]
assert rotate([(-1, -5)]) == [(-5, 1)]
assert rotate([(-5, 1)]) == [(1, 5)]
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 19

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_2d")
input = get_strings(raw_input)
assert execute(input) == 0
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("ANSWER CORRECT")
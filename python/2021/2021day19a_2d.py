#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
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
        space.add(beacon_in_space)

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
            current_tile.append((int(line_parts[0]), int(line_parts[1])))

    # this scanner is completed
    tiles.append(current_tile)

    return tiles

def rotate(tile):
    # tile: [ (x, y), (x, y) ]
    return [(y, -x) for (x, y) in tile]

def get_all_rotations(tile):

    all_rotations = [tile]

    for _ in range(3):
        tile = rotate(tile)
        all_rotations.append(tile)

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
    match_count = 0
    (ox, oy) = offset

    for (x, y) in tile:
        beacon_offset = (x + ox, y + oy)
        if beacon_offset in space:
            match_count += 1
    
    print(f"offset {offset} has {match_count} matches")

    if (match_count >= 3):
        return True
    else:
        return False

def check_overlap(space, tile):

    space_bounds = get_bounds(space)
    ((space_x_min, space_x_max), (space_y_min, space_y_max)) = space_bounds
    tile_bounds = get_bounds(tile)
    ((tile_x_min, tile_x_max), (tile_y_min, tile_y_max)) = tile_bounds

    start_ox = space_x_min - tile_x_max
    end_ox = space_x_max - tile_x_min 

    start_oy = space_y_max - tile_y_min
    end_oy = space_y_min - tile_y_max 

    step_x = 1 if end_ox >= start_ox else -1 
    step_y = 1 if end_oy >= start_oy else -1

    for ox in range(start_ox, end_ox, step_x):
        for oy in range (start_oy, end_oy, step_y):
            offset = (ox, oy)
            if overlap(space, tile, offset):
                return offset

    return None

def execute(input):
    print(input)

    tiles = parse_input(input) 

    space = set()
    
    # anchor the first tile
    next_tile = tiles[0]
    tiles.remove(next_tile)
    add_to_space(next_tile, (0, 0), space)
    print(f"Added another tile to space, space has {len(space)} beacons, {len(tiles)} tiles left...")

    # for all remaining tiles, try to fit them into the existing space
    while len(tiles) > 0:
        next_tile = tiles[0]
        tiles.remove(next_tile)
        tile_rotations = get_all_rotations(next_tile)
        offset = None        
        for next_tile_rotation in tile_rotations:
            offset = check_overlap(space, next_tile_rotation)
            if offset is not None:
                add_to_space(next_tile, offset, space)
                print(f"Added another tile to space, {len(tiles)} left...")
                break
        if offset is None:
            tiles.append(next_tile)

    # count the number of beacons in space
    result = len(space)
    print(f"result: {result}") 
    return result

# TESTS
assert rotate([(1, 5)]) == [(5, -1)]
assert rotate([(5, -1)]) == [(-1, -5)]
assert rotate([(-1, -5)]) == [(-5, 1)]
assert rotate([(-5, 1)]) == [(1, 5)]
assert overlap({(0, 2), (3, 3), (4, 1)}, [(-1, -1), (-5, 0), (-2, 1)], (5, 2)) == True
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 19

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_2d")
input = get_strings(raw_input)
assert execute(input) == 3
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("ANSWER CORRECT")
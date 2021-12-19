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
    print(f"Added {tile[0]} to space with offset: {offset}")
    for beacon in tile[1]:
        (x, y, z) = beacon
        (ox, oy, oz) = offset
        beacon_in_space = (x + ox, y + oy, z + oz)
        space.add(beacon_in_space)

def parse_input(input):

    cubes = []

    beacons = []
    cube_number = 0
    for line in input:
        if line[:3] == "---": # ignore the first line
            continue
        if line == "": # this scanner is completed
            cubes.append((f"Cube #{cube_number}", beacons))
            cube_number += 1
            beacons = []
        else:
            line_parts = line.split(",")
            beacon = (int(line_parts[0]), int(line_parts[1]), int(line_parts[2]))
            beacons.append(beacon)

    # this cube is completed
    cubes.append((f"Cube #{cube_number}", beacons))
    
    print(f"Loaded Cube: {cubes}")
    return cubes

def rotate(plane, tile):
    # tile: [ (x, y), (x, y) ]
    if plane[:2] == "xy":
        return (f"{tile[0]} {plane}", [(y, -x, z) for (x, y, z) in tile[1]])
    elif plane[:2] == "yz":
        return (f"{tile[0]} {plane}", [(x, z, -y) for (x, y, z) in tile[1]])
    elif plane[:2] == "xz":
        return (f"{tile[0]} {plane}", [(z, y, -x) for (x, y, z) in tile[1]])

def get_all_rotations(original_tile):
 
    all_rotations = [original_tile]

    tile = original_tile
    for _ in range(3):
        tile = rotate("xy", tile)
        all_rotations.append(tile)

    tile = original_tile
    for _ in range(3):
        tile = rotate("yz", tile)
        all_rotations.append(tile)

    tile = original_tile
    for _ in range(3):
        tile = rotate("xz", tile)
        all_rotations.append(tile)

    #flipped = get_flipped(tile)
    return all_rotations

def get_bounds(beacons):

    xs = [ x for (x, y, z) in beacons] 
    x_min = min(xs)
    x_max = max(xs)
    
    ys = [ y for (x, y, z) in beacons] 
    y_min = min(ys)
    y_max = max(ys)
    
    zs = [ z for (x, y, z) in beacons] 
    z_min = min(zs)
    z_max = max(zs)

    return ((x_min, x_max), (y_min, y_max), (z_min, z_max)) 

def overlap(space, beacons, offset):
    match_count = 0
    (ox, oy, oz) = offset

    for (x, y, z) in beacons:
        beacon_offset = (x + ox, y + oy, z + oz)
        if beacon_offset in space:
            match_count += 1
    
    #print(f"offset {offset} has {match_count} matches")

    if (match_count >= 3):
        return True
    else:
        return False

def check_overlap(space, cube):

    beacons = cube[1]

    space_bounds = get_bounds(space)
    ((space_x_min, space_x_max), (space_y_min, space_y_max), (space_z_min, space_z_max)) = space_bounds
    tile_bounds = get_bounds(beacons)
    ((tile_x_min, tile_x_max), (tile_y_min, tile_y_max), (tile_z_min, tile_z_max)) = tile_bounds

    start_ox = space_x_min - tile_x_max
    end_ox = space_x_max - tile_x_min 

    start_oy = space_y_max - tile_y_min
    end_oy = space_y_min - tile_y_max 

    start_oz = space_z_max - tile_z_min
    end_oz = space_z_min - tile_z_max 

    step_x = 1 if end_ox >= start_ox else -1 
    step_y = 1 if end_oy >= start_oy else -1
    step_z = 1 if end_oz >= start_oz else -1

    for ox in range(start_ox, end_ox, step_x):
        for oy in range (start_oy, end_oy, step_y):
            for oz in range (start_oz, end_oz, step_z):
                offset = (ox, oy, oz)
                if overlap(space, beacons, offset):
                    return offset

    return None

def execute(input):
    print(input)

    tiles = parse_input(input) 

    space = set()
    
    # anchor the first tile
    next_tile = tiles[0]
    tiles.remove(next_tile)
    add_to_space(next_tile, (0, 0, 0), space)
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
                print(f"Added another tile to space, space has {len(space)} beacons, {len(tiles)} tiles left...")
                break
        if offset is None: # we failed to place this tile, save it for later
            tiles.append(next_tile)

    # count the number of beacons in space
    result = len(space)
    print(f"result: {result}") 
    return result

# TESTS
# assert rotate([(1, 5)]) == [(5, -1)]
assert rotate("xy", ("test1", [(1, 2, 3)])) == ("test1 xy", [(2, -1, 3)])
assert rotate("yz", ("test1", [(1, 2, 3)])) == ("test1 yz", [(1, 3, -2)])
assert rotate("xz", ("test1", [(1, 2, 3)])) == ("test1 xz", [(3, 2, -1)])
# assert rotate([(5, -1)]) == [(-1, -5)]
# assert rotate([(-1, -5)]) == [(-5, 1)]
# assert rotate([(-5, 1)]) == [(1, 5)]
# assert overlap({(-1, -1, 1), (-2, -2, 2), (-3, -3, 3), (-2, -3, 1), (5, 6, -4), (8, 0, 7)}, [(1, -1, 1), (2, -2, 2), (3, -3, 3), (2, -1, 3), (-5, 4, -6), (-8, -7, 0)]) == True
# assert overlap({(0, 2), (3, 3), (4, 1)}, [(-1, -1), (-5, 0), (-2, 1)], (5, 2)) == True
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 19

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_3d_single_scanner")
input = get_strings(raw_input)
assert execute(input) == 6
print("TEST INPUT (single scanner) PASSED")

raw_input = get_input(YEAR, DAY, "_test_3d")
input = get_strings(raw_input)
assert execute(input) == 79
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("ANSWER CORRECT")
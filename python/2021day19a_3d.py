#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

class Cube():
    def __init__(self, name, beacons):
        self.name = name
        self.beacons = beacons

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
    print(f"Loaded Last Cube #{cube_number}")

    return cubes

# I totally cheated here!
# I spent hours trying to do the rotations logically but couldn't get it right so I gave up

rotation_functions = []
rotation_functions.append(lambda x, y, z: (x, y, z))
rotation_functions.append(lambda x, y, z: (x, z, -y))
rotation_functions.append(lambda x, y, z: (-z, x, -y))
rotation_functions.append(lambda x, y, z: (-x, -z, -y))
rotation_functions.append(lambda x, y, z: (z, -x, -y))
rotation_functions.append(lambda x, y, z: (z, -y, x))
rotation_functions.append(lambda x, y, z: (y, z, x))
rotation_functions.append(lambda x, y, z: (-z, y, x))
rotation_functions.append(lambda x, y, z: (-y, -z, x))
rotation_functions.append(lambda x, y, z: (-y, x, z))
rotation_functions.append(lambda x, y, z: (-x, -y, z))
rotation_functions.append(lambda x, y, z: (y, -x, z))
rotation_functions.append(lambda x, y, z: (-z, -x, y))
rotation_functions.append(lambda x, y, z: (x, -z, y))
rotation_functions.append(lambda x, y, z: (z, x, y))
rotation_functions.append(lambda x, y, z: (-x, z, y))
rotation_functions.append(lambda x, y, z: (-x, y, -z))
rotation_functions.append(lambda x, y, z: (-y, -x, -z))
rotation_functions.append(lambda x, y, z: (x, -y, -z))
rotation_functions.append(lambda x, y, z: (y, x, -z))
rotation_functions.append(lambda x, y, z: (y, -z, -x))
rotation_functions.append(lambda x, y, z: (z, y, -x))
rotation_functions.append(lambda x, y, z: (-y, z, -x))
rotation_functions.append(lambda x, y, z: (-z, -y, -x))

def get_all_rotations(cube):
 
    all_rotations = []

    for i, rotation_function in enumerate(rotation_functions):
        (original_cube_name, original_beacons) = cube
        rotated_cube_name = f"{original_cube_name} => {i}" # this is only useful for debugging
        rotated_beacons = [rotation_function(x, y, z) for (x, y, z) in original_beacons]
        rotated_cube = (rotated_cube_name, rotated_beacons)
        all_rotations.append(rotated_cube)

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

def overlap(space, beacons, offset, expected_match_count):
    match_count = 0
    (ox, oy, oz) = offset

    for (x, y, z) in beacons:
        beacon_offset = (x + ox, y + oy, z + oz)
        if beacon_offset in space:
            match_count += 1
    
    #print(f"offset {offset} has {match_count} matches")

    if (match_count >= expected_match_count):
        return True
    else:
        return False

def try_to_fit(space_beacons, cube_beacons, match_count):

    distances = {}
    
    # print(f"check_overlap: must do { len(cube_beacons) * len(space_beacons)} checks")

    for cube_beacon in cube_beacons:
        for space_beacon in space_beacons:
            dx = cube_beacon[0] - space_beacon[0]
            dy = cube_beacon[1] - space_beacon[1]
            dz = cube_beacon[2] - space_beacon[2]
            distance = (dx, dy, dz)
            if distance in distances:
                distances[distance] += 1
                if distances[distance] >= match_count:
                    offset = (-dx, -dy, -dz)
                    return offset
            else:
                distances[distance] = 1

    return None

def build_space(cubes, match_count):

    space = set()
    
    # anchor the first cube as the center of our space
    cube = cubes[0]
    cubes.remove(cube)
    add_to_space(cube, (0, 0, 0), space)

    # for all remaining cubes, try to fit them into the existing space
    while len(cubes) > 0:
        cube = cubes[0]
        cubes.remove(cube)
        cube_rotations = get_all_rotations(cube)
        offset = None        
        for rotated_cube in cube_rotations:
            (rotated_cube_name, rotated_beacons) = rotated_cube
            #print(f"Attempting to fit '{rotated_cube_name}'...")
            (cube_fits, offset) = try_to_fit(space, rotated_beacons, match_count)
            if cube_fits:
                add_to_space(rotated_cube, offset, space)
                break
        if offset is None: # after checking all rotations, we failed to place this cube, save it for later
            print(f"FAILED to fit '{cube[0]}' in any rotation... will try again later")
            cubes.append(cube)

    return space

def get_number_of_beacons(space):
    return len(space)

def execute(input, match_count = 12):

    cubes = parse_input(input) 
    space = build_space(cubes, match_count)
    result = get_number_of_beacons(space)

    print(f"result: {result}") 
    return result

# TESTS

# testing transformations with 0 offset

beacons = [(-1,-1,1), (-2,-2,2), (-3,-3,3), (-2,-3,1), (5,6,-4), (8,0,7)]
test_cube = ('TEST CUBE', beacons)
rotations = get_all_rotations(test_cube)
assert get_distinct_beacons(rotations, 6) == 6

# testing no transformations with (5,5,5) offset

test_cube0 = ('TEST CUBE 0', [(1,1,1), (2,2,2), (3,3,3)])
test_cube1 = ('TEST CUBE 1 + (5,5,5)', [(6,6,6), (7,7,7), (8,8,8)])
assert get_distinct_beacons([test_cube0, test_cube1], 3) == 3

print("ALL TESTS PASSED")

YEAR = 2021
DAY = 19

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_3d_single_scanner")
input = get_strings(raw_input)
assert execute(input, 6) == 6
print("TEST INPUT (single scanner) PASSED")

raw_input = get_input(YEAR, DAY, "_test_3d")
input = get_strings(raw_input)
assert execute(input) == 79
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 472
print("ANSWER CORRECT")
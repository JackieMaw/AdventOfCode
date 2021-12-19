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

# CHEAT!

transformation_functions = []
transformation_functions.append(lambda x, y, z: (x, z, -y))
transformation_functions.append(lambda x, y, z: (-z, x, -y))
transformation_functions.append(lambda x, y, z: (-x, -z, -y))

transformation_functions.append(lambda x, y, z: (z, -x, -y))
transformation_functions.append(lambda x, y, z: (z, -y, x))
transformation_functions.append(lambda x, y, z: (y, z, x))

transformation_functions.append(lambda x, y, z: (-z, y, x))
transformation_functions.append(lambda x, y, z: (-y, -z, x))
transformation_functions.append(lambda x, y, z: (-y, x, z))

transformation_functions.append(lambda x, y, z: (-x, -y, z))
transformation_functions.append(lambda x, y, z: (y, -x, z))
transformation_functions.append(lambda x, y, z: (x, y, z))

transformation_functions.append(lambda x, y, z: (-z, -x, y))
transformation_functions.append(lambda x, y, z: (x, -z, y))
transformation_functions.append(lambda x, y, z: (z, x, y))

transformation_functions.append(lambda x, y, z: (-x, z, y))
transformation_functions.append(lambda x, y, z: (-x, y, -z))
transformation_functions.append(lambda x, y, z: (-y, -x, -z))

transformation_functions.append(lambda x, y, z: (x, -y, -z))
transformation_functions.append(lambda x, y, z: (y, x, -z))
transformation_functions.append(lambda x, y, z: (y, -z, -x))

transformation_functions.append(lambda x, y, z: (z, y, -x))
transformation_functions.append(lambda x, y, z: (-y, z, -x))
transformation_functions.append(lambda x, y, z: (-z, -y, -x))

def get_all_rotations(cube):
 
    all_rotations = []

    for i, transformation_function in enumerate(transformation_functions):
        cube_name = f"{cube[0]} => {i}"
        beacons = [transformation_function(x, y, z) for (x, y, z) in cube[1]]
        all_rotations.append((cube_name, beacons))

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

def check_overlap(space_beacons, cube_beacons, match_count):

    distances = {}
    
    # print(f"check_overlap: must do { len(cube_beacons) * len(space_beacons)} checks")

    for cube_beacon in cube_beacons:
        for space_beacon in space_beacons:
            distance = (cube_beacon[0] - space_beacon[0], cube_beacon[1] - space_beacon[1], cube_beacon[2] - space_beacon[2])
            if distance in distances:
                distances[distance] += 1
                if distances[distance] >= match_count:
                    return distance
            else:
                distances[distance] = 1

    return None

def get_distinct_beacons(cubes, match_count):

    space = set()
    
    # anchor the first tile
    cube = cubes[0]
    cubes.remove(cube)
    add_to_space(cube, (0, 0, 0), space)

    # for all remaining cubes, try to fit them into the existing space
    while len(cubes) > 0:
        cube = cubes[0]
        cubes.remove(cube)
        cube_rotations = get_all_rotations(cube)
        offset = None        
        for cube_rotation in cube_rotations:
            print(f"Checking '{cube_rotation[0]}'...")
            offset = check_overlap(space, cube_rotation[1], match_count)
            if offset is not None:
                add_to_space(cube_rotation, offset, space)
                break
        if offset is None: # after checking all rotations, we failed to place this tile, save it for later
            print(f"FAILED to match '{cube[0]}' in any rotation... will try again later")
            cubes.append(cube)

    # count the number of beacons in space
    return len(space)

def execute(input, match_count = 12):
    #print(input)
    cubes = parse_input(input) 

    result = get_distinct_beacons(cubes, match_count)
    print(f"result: {result}") 
    return result

# TESTS
# assert rotate([(1, 5)]) == [(5, -1)]
# assert rotate("xy", ("test1", [(1, 2, 3)])) == ("test1 xy", [(2, -1, 3)])
# assert rotate("yz", ("test1", [(1, 2, 3)])) == ("test1 yz", [(1, 3, -2)])
# assert rotate("xz", ("test1", [(1, 2, 3)])) == ("test1 xz", [(3, 2, -1)])
# # assert rotate([(5, -1)]) == [(-1, -5)]
# # assert rotate([(-1, -5)]) == [(-5, 1)]
# # assert rotate([(-5, 1)]) == [(1, 5)]
# # assert overlap({(-1, -1, 1), (-2, -2, 2), (-3, -3, 3), (-2, -3, 1), (5, 6, -4), (8, 0, 7)}, [(1, -1, 1), (2, -2, 2), (3, -3, 3), (2, -1, 3), (-5, 4, -6), (-8, -7, 0)]) == True
# # assert overlap({(0, 2), (3, 3), (4, 1)}, [(-1, -1), (-5, 0), (-2, 1)], (5, 2)) == True


beacons = [(i, i+1, i+2) for i in range(1, 13)]
cube0 = ('Cube #0', beacons)
rotations = get_all_rotations(cube0)
assert get_distinct_beacons(rotations, 12) == 12

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
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("ANSWER CORRECT")
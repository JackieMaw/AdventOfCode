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
transformation_functions.append(lambda x, y, z: (x, y, z))

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

def get_max_distance(cubes, match_count):

    space = set()
    scanners = []
    
    # anchor the first tile at (0,0,0)
    cube = cubes[0]
    cubes.remove(cube)
    offset = (0, 0, 0)
    add_to_space(cube, offset, space)
    scanners.append(offset)

    # for all remaining cubes, try to fit them into the existing space
    while len(cubes) > 0:
        cube = cubes[0]
        cubes.remove(cube)
        cube_rotations = get_all_rotations(cube)
        offset = None        
        for cube_rotation in cube_rotations:
            #print(f"Checking '{cube_rotation[0]}'...")
            offset = check_overlap(space, cube_rotation[1], match_count)
            if offset is not None:
                add_to_space(cube_rotation, offset, space)
                scanners.append(offset)
                break
        if offset is None: # after checking all rotations, we failed to place this tile, save it for later
            #print(f"FAILED to match '{cube[0]}' in any rotation... will try again later")
            cubes.append(cube)

    # count the number of beacons in space
    # return len(space)

    return calc_max_distance(scanners)

def calc_max_distance(scanners):
    max_distance = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            if scanner1 != scanner2:
                distance = abs(scanner1[0] - scanner2[0]) + abs(scanner1[1] - scanner2[1]) + abs(scanner1[2] - scanner2[2])
                if distance > max_distance:
                    max_distance = distance
    return max_distance

def execute(input, match_count = 12):
    #print(input)
    cubes = parse_input(input) 

    result = get_max_distance(cubes, match_count)
    print(f"result: {result}") 
    return result

# TESTS
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 19

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_3d_single_scanner")
input = get_strings(raw_input)
assert execute(input, 6) == 0
print("TEST INPUT (single scanner) PASSED")

raw_input = get_input(YEAR, DAY, "_test_3d")
input = get_strings(raw_input)
assert execute(input) == 3621
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 12092
print("ANSWER CORRECT")
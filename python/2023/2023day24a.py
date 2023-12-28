from utilities import *
import math
import copy
import itertools

def get_line(line_info):

    (point, slope) = line_info
    # y = mx + c

    (x, y) = point
    (sx, sy) = slope
    m = sy / sx
    c = y - m*x

    print(f"{(m, c)}: y = {m}x + {c}")
    return (point, slope, m, c)

def get_intersection_of_lines(line1, line2, target_range):
    (p1, s1, m1, c1) = line1
    (p2, s2, m2, c2) = line2
    print(f"y = {m1}x + {c1} <<<<>>>> y = {m2}x + {c2}")
    
    if (m1 - m2) == 0:
        print("Hailstones' paths are parallel; they never intersect.")
        return None
    
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    (range_start, range_end) = target_range
    if x < range_start or x > range_end or y < range_start or y > range_end:
        print(f"Hailstones' paths will cross outside the test area (at x={x:.2f}, y={y:.2f}).")
        return None
    
    (x1, y1) = p1
    (sx1, sy1) = s1

    (x2, y2) = p2
    (sx2, sy2) = s2

    in_the_future1 = ((x - x1)/sx1) > 0
    in_the_future2 = ((x - x2)/sx2) > 0

    if not in_the_future1:
        print(f"Hailstones' paths crossed in the past for hailstone A.")
        return None
    elif not in_the_future2:
        print(f"Hailstones' paths crossed in the past for hailstone B.")
        return None
    else:
        print(f"Hailstones' paths will cross inside the test area (at x={x:.2f}, y={y:.2f}).")
        return (x, y)


def parse_point(input_line):
    line_parts = input_line.split("@")
    point_parts = line_parts[0].split(",")
    point = (int(point_parts[0].strip()), int(point_parts[1].strip()))
    slope_parts = line_parts[1].split(",")
    slope = (int(slope_parts[0].strip()), int(slope_parts[1].strip()))
    return (point, slope)

def parse_input(input_lines):
    return [get_line(parse_point(input_line)) for input_line in input_lines]

def get_num_intersections(lines, target_range):

    num_intersections = 0

    combos = list(itertools.combinations(lines, 2))
    print(f"{len(lines)} lines have {len(combos)} possible intersections")
    for (line1, line2) in combos:
        intersection = get_intersection_of_lines(line1, line2, target_range)
        if intersection is not None:
            num_intersections += 1

    return num_intersections

def execute(input_lines, target_range):
    print(input_lines)
    lines = parse_input(input_lines)
    result = get_num_intersections(lines, target_range)
    print(f"result: {result}")
    return result

# TESTS
line1 = ((19, 13), (-2, 1), -0.5, 22.5)
line2 = ((18, 19), (-1, -1), 1, 1)
assert get_line(((19, 13), (-2, 1))) == line1
assert get_line(((18, 19), (-1, -1))) == line2
assert get_intersection_of_lines(line1, line2, (7, 27)) == (14.333333333333334, 15.333333333333332)
assert get_intersection_of_lines(line1, line2, (20, 27)) == None
print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 24

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines, (7, 27)) == 2
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines, (200000000000000, 400000000000000)) == 16589
print("ANSWER CORRECT")
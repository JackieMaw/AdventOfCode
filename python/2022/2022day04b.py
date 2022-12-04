from utilities import *

def get_range(r):
    #88-99
    return [int(part) for part in r.split("-")]

def get_ranges(pair):
    #88-99,64-97
    return [get_range(part) for part in pair.split(',')]

def point_lies_within(p, range):
    return p >= range[0] and p <= range[1]

def overlaps(ranges):
    r1 = ranges[0]
    r2 = ranges[1]
    return partially_inside(r1, r2) or partially_inside(r2, r1)

def partially_inside(r1, r2):
    return point_lies_within(r1[0], r2) or point_lies_within(r1[1], r2)

def execute(input):
    result = sum([overlaps(get_ranges(pair)) for pair in input])
    print(f"result: {result}") 
    return result

# TESTS
assert get_ranges('88-99,64-97') == [[88, 99], [64, 97]]
assert overlaps([[88, 99], [64, 97]]) == True
assert overlaps([[2, 8], [3, 7]]) == True
assert overlaps([[3, 7], [2, 8]]) == True
print("ALL TESTS PASSED")

YEAR = 2022
DAY = 4

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 837
print("ANSWER CORRECT")
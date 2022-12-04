from utilities import *

def get_range(r):
    #88-99
    return [int(part) for part in r.split("-")]

def get_ranges(pair):
    #88-99,64-97
    return [get_range(part) for part in pair.split(',')]

def contains_completely(ranges):
    r1 = ranges[0]
    r2 = ranges[1]
    return range_contains_completely(r1, r2) or range_contains_completely(r2, r1)

def range_contains_completely(r1, r2):
    return r1[0] <= r2[0] and r1[1] >= r2[1]

def execute(input):
    result = sum([contains_completely(get_ranges(pair)) for pair in input])
    print(f"result: {result}") 
    return result

# TESTS
assert get_ranges('88-99,64-97') == [[88, 99], [64, 97]]
assert contains_completely([[88, 99], [64, 97]]) == False
assert contains_completely([[2, 8], [3, 7]]) == True
assert contains_completely([[3, 7], [2, 8]]) == True
print("ALL TESTS PASSED")

YEAR = 2022
DAY = 4

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 450
print("ANSWER CORRECT")
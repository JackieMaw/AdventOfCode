from utilities import *
import math
import copy

def parse_input(input_lines):
    return None

def solve(initial_state):
    return 0

def execute(all_text):
    print(all_text)
    result = solve(all_text)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 0

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings_csv(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
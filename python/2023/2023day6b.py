import numpy
from utilities import *
import math
import copy

def parse_input(input_lines):
    times = int(''.join(input_lines[0].split(":")[1].split()))
    distances = int(''.join(input_lines[1].split(":")[1].split()))
    return (times, distances)

def execute(input):
    print(input)
    result = 0

    (winning_time, winning_distance) = parse_input(input)
    
    print(f"ONE BIG RACE: ({winning_time}, {winning_distance})....")

    num_wins = 0
    for hold_button in range(1, winning_time- 1):
        distance_travelled = hold_button * (winning_time - hold_button)
        if distance_travelled > winning_distance:
            num_wins += 1
    
    result = num_wins

    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 6

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 71503
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 36992486
print("ANSWER CORRECT")
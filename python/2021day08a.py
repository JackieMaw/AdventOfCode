#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def count_unique_output_values(input):
    count = 0
    for s in input:
        sparts = s.split("|")
        signals = sparts[0].split()
        output = sparts[1].split()
        for output_value in output:
            if len(output_value) in [2,4,3,7]:
                count += 1
    return count

def execute(input):
    #print(input)

    result = count_unique_output_values(input)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 8

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 26
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 383
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):

    increases = 0
    for i in range(len(input) - 3):
        sum1 =  input[i] + input [i+1] + input [i+2]
        sum2 =  input[i+1] + input [i+2] + input [i+3]
        diff = sum2 - sum1
        if (diff > 0):
            increases += 1

    return increases

# TESTS
#assert execute(get_strings_csv(["ABCD"])) == 0
#print("ALL TESTS PASSED")

# REAL INPUT DATA
YEAR = 2021
DAY = 1
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers(raw_input)
assert execute(input) == 1748
print("ANSWER CORRECT")
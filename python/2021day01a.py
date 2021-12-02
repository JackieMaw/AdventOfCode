#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):

    increases = 0
    for i in range(len(input) - 1):
        diff = input[i+1] - input[i]
        if (diff > 0):
            increases += 1

    return increases

# REAL INPUT DATA
YEAR = 2021
DAY = 1
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers(raw_input)
print(execute(input))
assert execute(input) == 1722
print("ANSWER CORRECT")
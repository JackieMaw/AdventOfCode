#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):
    return 0

assert execute(get_strings_csv(["ABCD"])) == 0
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 4
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings_csv(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
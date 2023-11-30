from utilities import *
import math
import copy

def execute(input):
    print(input)
    stack = []
    pos = 0
    for i in input:
        pos += 1
        if i == '(':
            stack.append(i)
        elif len(stack) == 0:
            break
        else:
            stack.pop()
    result = pos
    print(f"result: {result}")
    return result

# TESTS
assert execute(get_strings([")"])[0]) == 1
assert execute(get_strings(["()())"])[0]) == 5
print("ALL TESTS PASSED")

YEAR = 2015
DAY = 1

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input[0]) == 0
print("ANSWER CORRECT")
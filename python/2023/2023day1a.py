from utilities import *
import math
import copy

def execute(input):
    print(input)

    sum = 0    

    for line in input:
        digits = ""
        for char in line:
            if char.isdigit():
                digits += char
        sum += int(digits[0] + digits[-1])

    result = sum
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 1

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 55090
print("ANSWER CORRECT")
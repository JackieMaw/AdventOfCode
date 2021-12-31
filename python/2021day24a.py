#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

function_cache = {}

def function(w, divisor, param1, param2, z):
    params = (w, divisor, param1, param2, z)
    if params in function_cache:
        return function_cache[params]
    else:
        result = exec_function(w, divisor, param1, param2, z)
        function_cache[params] = result
        return result

def exec_function(w, divisor, param1, param2, z):
    x = 0 if (z % 26 + param1) == w else 1
    y1 = 25 * x + 1
    z = (z // divisor) * y1
    y2 = (w + param2) * x
    return z + y2

def check_number(number):

    digits = [int(digit) for digit in str(number)]

    if 0 in digits:
        return False

    # if digits[12] not in [1, 2]:
    #     return False

    z = function(digits[0], 1, 12, 6, 0)
    z = function(digits[1], 1, 11, 12, z)
    z = function(digits[2], 1, 10, 5, z)
    z = function(digits[3], 1, 10, 10, z)

    z = function(digits[4], 26, -16, 7, z)
    
    z = function(digits[5], 1, 14, 0, z)
    z = function(digits[6], 1, 12, 4, z)

    z = function(digits[7], 26, -4, 12, z)

    z = function(digits[8], 1, 15, 14, z)

    z = function(digits[9], 26, -7, 13, z)
    z = function(digits[10], 26, -8, 10, z)
    z = function(digits[11], 26, -4, 11, z)
    z = function(digits[12], 26, -15, 9, z)
    z = function(digits[13], 26, -8, 9, z)

    model_number_accepted = z == 0

    if model_number_accepted:
        print(f"Model Number Accepted: {number}")
    # else:
    #     print(f"Model Number Rejected: {number}")

    return model_number_accepted

def execute():
    
    # what happens with different values of z
    # for w1 in range(1,10):
    #     z1 = f1(w1, 1, 12, 6, 0)
    #     print(f"f1({w1}, 1, 12, 6, 0) => {z1}") 
    #     for w2 in range(1,10):
    #         z2 = f1(w2, 1, 11, 12, z1)
    #         print(f"    f1({w2}, 1, 11, 12, {z1}) => {z2}") 

    #number = [ 9 for _ in range(14)]   

    print(f"Trying to find the LARGEST MODEL NUMBER...") 
    for number in range(99999999999999, 11111111111111 - 1, -1):
        model_number_accepted = check_number(number)
        if model_number_accepted:
            result = number
            break
    
    print(f"LARGEST MODE bL NUMBER ACCEPTED: {result}") 
    print()

    print(f"Trying to find the SMALLEST MODEL NUMBER...") 
    for number in range(11111111111111, 99999999999999 + 1, +1):
        model_number_accepted = check_number(number)
        if model_number_accepted:
            result = number
            break
    
    print(f"SMALLEST MODEL NUMBER ACCEPTED: {result}") 

# CHECK THE FINAL FORMULA

# pairs = [(z12, z12 - 8) for z12 in range(9, 18)]
# for (z12, w) in pairs:
#     z13 = function(w, 26, -8, 9, z12)
#     assert z13 == 0

# print(f"z13 Sanity Check Passed, yay!")

# # z = 9 * 26 to 18 * 26 - 1
# # w = (z11 mod 26) - 15

# valid_digits = list(range(1, 10))
# for z11 in range(9 * 26, 18 * 26):
#     w = (z11 // 26) - 15 
#     if w in valid_digits:
#         print(f"{(z11, w)}")

# print(f"z11 Generation Completed")


# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 24

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
execute()
print()
print(f"Press ENTER to continue...")
user_input = input()
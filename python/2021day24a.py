#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def f1(w, divisor, param1, param2, z):
    x = 0 if (z ** 26 + param1) == w else 1
    y1 = 25 * x + 1
    z = z // divisor * y1
    y2 = (w + param2) * x
    return z + y2

def check_number(number):

    if 0 in number:
        return False

    z = f1(number[0], 1, 12, 6, 0)
    z = f1(number[1], 1, 11, 12, z)
    z = f1(number[2], 1, 10, 5, z)
    z = f1(number[3], 1, 10, 10, z)

    z = f1(number[4], 26, -16, 7, z)
    
    z = f1(number[5], 1, 14, 0, z)
    z = f1(number[6], 1, 12, 4, z)

    z = f1(number[7], 26, -4, 12, z)

    z = f1(number[8], 1, 15, 14, z)

    z = f1(number[9], 26, -7, 13, z)
    z = f1(number[10], 26, -8, 10, z)
    z = f1(number[11], 26, -4, 11, z)
    z = f1(number[12], 26, -15, 9, z)
    z = f1(number[13],26,  -8, 9, z)

    model_number_accepted = z == 0

    if model_number_accepted:
        print(f"Model Number Accepted: {number}")
    else:
        print(f"Model Number Rejected: {number}")

def execute():
    
    # what happens with different values of z
    for w1 in range(1,10):
        z1 = f1(w1, 1, 12, 6, 0)
        print(f"f1({w1}, 1, 12, 6, 0) => {z1}") 
        for w2 in range(1,10):
            z2 = f1(w2, 1, 11, 12, z1)
            print(f"    f1({w2}, 1, 11, 12, {z1}) => {z2}") 

    #number = [ 9 for _ in range(14)]   

    for number in range(99999999999999, 11111111111111, -1):
        number_list = [int(digit) for digit in str(number)]
        model_number_accepted = check_number(number_list)
        if model_number_accepted:
            result = number
            break
        
    print(f"result: {result}") 
    return result

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
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute() == 0
print("ANSWER CORRECT")
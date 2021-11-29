#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):
    start, end = input[0].split("-")
    # It is a six-digit number.
    # ==> this should be solved at generation time
    # The value is within the range given in your puzzle input. 
    # ==> this should be solved at generation time
    number = int(start)
    valid = 0
    while number <= int(end):
        number += 1
        if is_valid_password(number):
            valid += 1
    return valid

def is_valid_password(number):
    s = str(number)

    found_twins = False
    for i in range(5):
        # Two adjacent digits are the same (like 22 in 122345).    
        if (s[i] == s[i+1]):
            found_twins = True  
        # Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679). 
        if (int(s[i]) > int(s[i+1])):
            return False #immediately exit

    return found_twins

def find_twins(s):
    
    return False

# TODO - is there a better way to write my tests?
assert is_valid_password(111111) == True
assert is_valid_password(223450) == False
assert is_valid_password(123789) == False
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 4
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 2779
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

def grow(register):
    new_register = register.copy()
    for i in range(0, 8):
        new_register[i] = register[i+1]
    new_register[8] = register[0]
    new_register[6] = new_register[6] + register[0]
    #print(f"{register} => {new_register}")
    return new_register

def load_register(input):
    register = [0,0,0,0,0,0,0,0,0]
    for i in input:
        register[i] += 1
    #print(f"INITIAL REGISTER: {register}")
    return register

def execute(input, num_days):
    print(input)

    register = load_register(input)

    for i in range(num_days):
        register = grow(register)
        #print(f"day {i}: {sum(register)}") 

    result = sum(register)
    print(f"result: {result}") 
    return result

# TESTS
# custom test
initial = load_register(get_integers_csv(["0,1,2,3,4,5,6,7,8"]))
after1day = grow(initial)
after1day_expected = load_register(get_integers_csv(["6,0,1,2,3,4,5,6,7,8"]))
print(f"after1day:          {after1day} => sum: {sum(after1day)}")
print(f"after1day_expected: {after1day_expected} => sum: {sum(after1day_expected)}")
assert after1day == after1day_expected
# day 0 test
day0 = load_register(get_integers_csv(["3,4,3,1,2"]))
day1 = grow(day0)
day1_expected = load_register(get_integers_csv(["2,3,2,0,1"]))
print(f"day1:          {day1} => sum: {sum(day1)}")
print(f"day1_expected: {day1_expected} => sum: {sum(day1_expected)}")
assert day1 == day1_expected
# day 10 test
day10 = load_register(get_integers_csv(["0,1,0,5,6,0,1,2,2,3,7,8"]))
day11 = grow(day10)
day11_expected = load_register(get_integers_csv(["6,0,6,4,5,6,0,1,1,2,6,7,8,8,8"]))
print(f"day11:          {day11} => sum: {sum(day11)}")
print(f"day11_expected: {day11_expected} => sum: {sum(day11_expected)}")
assert day11 == day11_expected
# day 17 test
day17 = load_register(get_integers_csv(["0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8"]))
day18 = grow(day17)
day18_expected = load_register(get_integers_csv(["6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8"]))
print(f"day18:          {day18} => sum: {sum(day18)}")
print(f"day18_expected: {day18_expected} => sum: {sum(day18_expected)}")
assert day18 == day18_expected
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 6

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_integers_csv(raw_input)
assert execute(input, 18) == 26
assert execute(input, 80) == 5934
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers_csv(raw_input)
assert execute(input, 80) == 366057
print("ANSWER CORRECT")
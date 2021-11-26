from utilities import *
import math

def execute(input_data):
    sum = 0
    for mass in input_data:
        sum += fuel_required(mass)
    return sum

def fuel_required(mass):
    return math.floor(mass / 3) - 2

assert fuel_required(12) == 2
assert fuel_required(14) == 2
assert fuel_required(1969) == 654
assert fuel_required(100756) == 33583
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 1
#download_input(YEAR, DAY)
#input_data = get_strings(YEAR, DAY)
input_data = get_integers(YEAR, DAY)
print(execute(input_data))
#3270338
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def get_frequencies(input):
    frequencies = {}
    for i in input:
        if i in frequencies:
            frequencies[i] += 1
        else:
            frequencies[i] = 1
    # print(frequencies)
    return frequencies 

def get_weighted_average(frequencies):
    sum = 0
    weighted_average = 0
    for i, f in frequencies.items():
        sum += f
        weighted_average += i * f 
    return weighted_average / sum

def get_fuel_cost_to_move(n):
    return (n * (n + 1))/2

def calc_fuel(frequencies, position):
    fuel = 0
    for i, f in frequencies.items():
        distance = abs(i - position)
        this_fuel = get_fuel_cost_to_move(distance) * f
        # print(f"Move from {i} to {position}: {this_fuel} fuel")
        fuel += this_fuel
    return fuel

def find_smallest_move(frequencies, min, max):
    min_fuel = 99999999999
    best_position = 0
    for position in range(min, max + 1):
        fuel = calc_fuel(frequencies, position)
        if (fuel < min_fuel):
            min_fuel = fuel
            best_position = position
    print(f"min_fuel: {min_fuel}") 
    print(f"best_position: {best_position}") 
    return min_fuel

def execute(input):
    f = get_frequencies(input)

    min_position = min(input)
    max_position = max(input)

    result = find_smallest_move(f, min_position, max_position)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 7

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_integers_csv(raw_input)
f = get_frequencies(input)
assert f[0] == 1
assert f[1] == 2
assert f[14] == 1
assert f[16] == 1
assert get_fuel_cost_to_move(11) == 66
assert get_fuel_cost_to_move(4) == 10
assert execute(input) == 168
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers_csv(raw_input)
assert execute(input) == 100727924
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

def parse_input(input):
    mystring = input[0]

    steps = {}
    for line in input[2:]:
        line_parts = line.split(" -> ")
        steps[line_parts[0]] = line_parts[1]

    return mystring, steps

def transform(mystring, steps):

    newstring = []
    newstring.append(mystring[0])
    for i in range(len(mystring)-1):
        pair = "".join(mystring[i:i+2])
        if pair in steps:
            newstring.append(steps[pair])
        newstring.append(mystring[i+1])

    return newstring

def get_frequencies(mystring):

    frequencies = {}

    for char in mystring:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    return frequencies

def get_answer(frequencies):
    most_common = 0
    least_common = 999999

    for count in frequencies.values():
        if count > most_common:
            most_common = count
        if count < least_common:
            least_common = count

    return most_common - least_common

def execute(input, num_steps):
    print(input)

    mystring, steps = parse_input(input)

    for i in range(num_steps):
        mystring = transform(mystring, steps)
        print(f"after step: {i} mystring: {mystring}")

    frequencies = get_frequencies(mystring)

    result = get_answer(frequencies)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 14

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input, 10) == 1588
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input, 10) == 2509
print("ANSWER CORRECT")
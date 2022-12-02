#TODO - how to share utilities across folders? do I need to make a package?
from os import execl, system
from utilities.utilities import *
import math
import copy

def parse_input(input):
    mystring = input[0]

    mypairs = {}
    for i in range(len(mystring)-1):
        pair = "".join(mystring[i:i+2])
        
        if pair in mypairs:
            mypairs[pair] += 1
        else:
            mypairs[pair] = 1

    steps = {}
    for line in input[2:]:
        line_parts = line.split(" -> ")
        steps[line_parts[0]] = line_parts[1]

    return mystring, mypairs, steps

def transform(mypairs, steps):

    newpairs = mypairs.copy()
    for (pair, freq) in mypairs.items():
        if pair in steps:
            add(pair, newpairs, -freq)
            char = steps[pair]
            pair1 = pair[0] + char
            pair2 = char + pair[1]
            add(pair1, newpairs, freq)
            add(pair2, newpairs, freq)

    return newpairs

def add(key, dic, num):    
    if key in dic:
        dic[key] += num
    else:
        dic[key] = num

def check_frequencies(frequencies):  
    for (pair, freq) in frequencies.items():
        if (freq % 2 == 1):
            print(f"WARNING - Odd Frequency: {pair} => {freq}")

def get_frequencies(mystring, mypairs):    

    frequencies = {}

    # every character will be stored twice except for the first and last character
    first = mystring[0]
    last = mystring[-1]
    add(first, frequencies, 1)
    add(last, frequencies, 1)

    for (pair, freq) in mypairs.items():
        char1 = pair[0]
        add(char1, frequencies, freq)
        char2 = pair[1]
        add(char2, frequencies, freq)

    check_frequencies(frequencies)

    return frequencies

def get_answer(frequencies):
    most_common = list(frequencies.values())[0]
    least_common = most_common

    for count in frequencies.values():
        if count > most_common:
            most_common = count
        if count < least_common:
            least_common = count

    return (most_common / 2) - (least_common / 2)

def get_length(frequencies):
    return sum(frequencies.values()) / 2

def execute(input, num_steps):
    print(input)

    mystring, mypairs, steps = parse_input(input)
    frequencies = get_frequencies(mystring, mypairs)
    length = get_length(frequencies)
    print(f"before any steps, string length: {length}")

    for i in range(num_steps):
        mypairs = transform(mypairs, steps)
        frequencies = get_frequencies(mystring, mypairs)
        length = get_length(frequencies)
        print(f"after step: {i}, string length: {length}")

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
assert execute(input, 0) == 1
assert execute(input, 1) == 1
assert execute(input, 2) == 5
assert execute(input, 10) == 1588
assert execute(input, 40) == 2188189693529
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input, 10) == 2509
assert execute(input, 40) == 2827627697643
print("ANSWER CORRECT")
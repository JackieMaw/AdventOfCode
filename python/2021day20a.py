#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def parse_input(input):

    image_lookup = input[0]

    image = set()
    y = 0
    for line in input[2:]:
        x = 0
        for char in line:
            if char == "#":
                image.add((x, y))
            x += 1
        y += 1

    return image_lookup, image

def get_image_key(x, y, image):

    key = ""

    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if (i, j) in image:
                key += "1"
            else:                
                key += "0"
    
    return int(key, 2)

def play(image_lookup, image):

    xs = [ x for (x, y) in image] 
    x_min = min(xs)
    x_max = max(xs)
    
    ys = [ y for (x, y) in image] 
    y_min = min(ys)
    y_max = max(ys)

    new_image = set()
    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            key = get_image_key(x, y, image)
            pixel = image_lookup[key]
            if pixel == "#":
                new_image.add((x, y))
    
    return new_image

def execute(input):
    image_lookup, image = parse_input(input)

    print(f"Before any rounds, image has {len(image)} pixels")

    for i in range(2):
        image = play(image_lookup, image)
        print(f"After round {i}, image has {len(image)} pixels")

    result = len(image)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 20

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 35
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
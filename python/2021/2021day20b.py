#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def parse_input(input):

    image_lookup = input[0]

    image = set()
    y = 0    
    #print()
    for line in input[2:]:
        #print(line)
        x = 0
        for char in line:
            if char == "#":
                image.add((x, y))
            x += 1
        y += 1
    #print()
    return image_lookup, image

def get_image_key(x, y, image, x_min, x_max, y_min, y_max, unexplored_value):

    key = ""

    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            unexplored = i < x_min or i > x_max or j < y_min or j > y_max
            if unexplored:
                key += unexplored_value
            elif (i, j) in image:
                key += "1"
            else:                
                key += "0"
    
    return int(key, 2)

def play(image_lookup, image, unexplored_value):

    xs = [ x for (x, y) in image] 
    x_min = min(xs)
    x_max = max(xs)
    
    ys = [ y for (x, y) in image] 
    y_min = min(ys)
    y_max = max(ys)
    
    print(f"PLAY: {x_min - 1}  => {x_max + 1}, {y_min - 1}  => {y_max + 1}")

    new_image = set()
    #print()
    for y in range(y_min - 1, y_max + 2):
        line = ""
        for x in range(x_min - 1, x_max + 2):
            key = get_image_key(x, y, image, x_min, x_max, y_min, y_max, unexplored_value)
            pixel = image_lookup[key]
            line += pixel
            if pixel == "#":
                new_image.add((x, y))
        #print(line)
    #print()

    return new_image

def execute(input):
    image_lookup, image = parse_input(input)

    print(f"Before any rounds, image has {len(image)} pixels")

    alternating = image_lookup[0] == "#" and image_lookup[-1] == "."
    if alternating:
        print(f"WARNING: FLASHING DETECTED")

    for i in range(50):
        unexplored_value = "1" if alternating and i % 2 == 1 else "0"
        image = play(image_lookup, image, unexplored_value)
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
assert execute(input) == 3351
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 18989
print("ANSWER CORRECT")
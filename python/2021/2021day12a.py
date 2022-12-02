#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

def get_paths(input):

    paths = {}
    for line in input:
        parts = line.split("-")
        a = parts[0]
        b = parts[1]
        if a in paths:
            paths[a].append(b)
        else:
            paths[a] = [b]
        if b in paths:
            paths[b].append(a)
        else:
            paths[b] = [a]

    print(paths)
    return paths

def traverse(this, paths, history):

    history.append(this)

    all_paths = []
    # base case
    if (this == "end"):
        all_paths.append([this])
    else:
    # traverse children
        children = paths[this]
        for child in children:
            if not child.islower() or child not in history:  # this is horrible!
                paths_from_child = traverse(child, paths, history.copy())
                for path_from_child in paths_from_child:
                    path_from_child.insert(0, this)
                    all_paths.append(path_from_child)
    return all_paths

def get_number_of_paths(paths):

    history = []
    all_paths = traverse("start", paths, history)

    return len(all_paths)

def execute(input):
    print(input)

    paths = get_paths(input)

    number_of_paths = get_number_of_paths(paths)

    result = number_of_paths
    print(f"result: {result}") 
    return result

# TESTS
assert get_number_of_paths({"start" : ["end"]}) == 1
assert get_number_of_paths({"start" : ["a"], "a" : ["end"]}) == 1
assert get_number_of_paths({"start" : ["a", "b"], "a" : ["end"], "b" : ["end"]}) == 2
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 12

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 10
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 19
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 226
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 3292
print("ANSWER CORRECT")
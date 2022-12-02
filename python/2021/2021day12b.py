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

    for path in paths.values():
        path.sort()

    #print(paths)
    return paths

def can_i_visit_again(child, history, free_pass):
    if child == "start":
        return False
    if child == "end":
        return True
    if not child.islower():
        return True
    # special case, if this is lower case, and we already visited once, we can visit again but we only get one free pass for all the small caves
    if history.count(child) >= 1:
        #print(f"{history} => can we visit [{child}] again?")   
        if len(free_pass) == 0:
            free_pass.append(child)
            #print(f"YES - FREE PASS FOR [{child}] !")   
            return True
        else:
            return False
    else:
        return True

def traverse(this, paths, history, free_pass):

    history.append(this)

    all_paths = []
    # base case
    if (this == "end"):
        all_paths.append([this])
    else:
    # traverse children
        children = paths[this]
        for child in children:
            free_pass_for_child = free_pass.copy()
            if can_i_visit_again(child, history, free_pass_for_child):
                paths_from_child = traverse(child, paths, history.copy(), free_pass_for_child)
                for path_from_child in paths_from_child:
                    path_from_child.insert(0, this)
                    all_paths.append(path_from_child)
    
    #print(f"{history}  => {len(all_paths)} paths to end")
    #print(all_paths)
    return all_paths

def print_paths(all_paths):
    print(f"{len(all_paths)} PATHS FOUND:")
    for path in all_paths:
        print(",".join(path))

def get_number_of_paths(paths):

    history = []
    free_pass = []
    all_paths = traverse("start", paths, history, free_pass)

    #print_paths(all_paths)

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
assert execute(input) == 36
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 103
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 3509
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 89592
print("ANSWER CORRECT")
from utilities import *
import math
import copy

#'GTK = (BQR, PFH)'
def parse_node(line_parts):
    line_parts = line_parts.split('=')
    parent = line_parts[0].strip()
    child_parts = line_parts[1].replace('(', '').replace('(', '').strip().split(',')
    left = child_parts[0]
    right = child_parts[1]
    return (parent, left, right)

def parse_input(input_lines):
    instructions = input_lines[0]
    node_map = { node[0]: node for node in [parse_node(line) for line in input_lines[2:]] }
    return (instructions, node_map)

def get_num_steps(instructions, node_map):
    return len(instructions)

def execute(input_lines):
    print(input_lines)
    (instructions, node_map) = parse_input(input_lines)
    result = get_num_steps(instructions, node_map)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 8

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 2
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 6
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
from utilities import *




#'GTK = (BQR, PFH)'
def parse_node(line_parts):
    line_parts = line_parts.split('=')
    parent = line_parts[0].strip()
    child_parts = line_parts[1].replace('(', '').replace(')', '').strip().split(',')
    left = child_parts[0].strip()
    right = child_parts[1].strip()
    return (parent, left, right)

def parse_input(input_lines):
    instructions = input_lines[0]
    node_map = { node[0]: node for node in [parse_node(line) for line in input_lines[2:]] }
    return (instructions, node_map)

movement_cache = []

def get_next_node(current_node, instruction, node_map):    
    (parent, left, right) = node_map[current_node]
    if instruction == 'L':
        current_node = left
    elif instruction == 'R':
        current_node = right
    else:
        raise Exception(f"Unhandled case - instruction: {instruction}")
    return current_node

def get_all_starting_nodes(node_map):
    return list(filter(lambda node: node[-1] == "A", node_map.keys()))

def all_nodes_end_in_z(current_nodes):
    return all(node[-1] == "Z" for node in current_nodes)       

def get_num_steps(instructions, node_map):
    num_steps = 0
    current_nodes = get_all_starting_nodes(node_map)
    while True:
        for instruction in instructions:
            num_steps += 1
            print(f"{num_steps} >> {current_nodes}")
            current_nodes = [get_next_node(current_node, instruction, node_map) for current_node in current_nodes]         
            if all_nodes_end_in_z(current_nodes):
                return num_steps
        
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
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 6
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
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

def get_next_node(current_node, instructions, node_map, movement_cache): 

    next_node = None

    if (current_node, instructions) in movement_cache:      
        next_node = movement_cache[(current_node, instructions)]  
        #if len(instructions) > 1:
        #    print(f"CACHE HIT ({current_node}, {instructions}) >> {next_node}")
    else:
        #print(f"CACHE MISS ({current_node}, {instructions}) >> ???")
        if len(instructions) == 1:
            (parent, left, right) = node_map[current_node]
            if instructions == 'L':
                next_node = left
            elif instructions == 'R':
                next_node = right
            else:
                raise Exception(f"Unhandled case - instruction: {instruction}")
        else:
            next_node = get_next_node(current_node, instructions[0], node_map, movement_cache)
            next_node = get_next_node(next_node, instructions[1:], node_map, movement_cache)

        movement_cache[(current_node, instructions)] = next_node
        #print(f"CACHE UPDATED ({current_node}, {instructions}) >> {next_node}")

    return next_node

def get_all_starting_nodes(node_map):
    return list(filter(lambda node: node[-1] == "A", node_map.keys()))

def all_nodes_end_in_z(current_nodes):
    return all(node[-1] == "Z" for node in current_nodes)       

def get_num_steps(instructions, node_map):
    num_steps = 0
    movement_cache = {}
    current_nodes = get_all_starting_nodes(node_map)
    while True:
        #print(f"{num_steps} >> {current_nodes}")
        current_nodes = [get_next_node(current_node, instructions, node_map, movement_cache) for current_node in current_nodes]              
        num_steps += len(instructions)
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
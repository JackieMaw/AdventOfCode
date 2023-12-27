import random
from utilities import *
import math
import copy

def parse_input(input_lines):

    node_map = {}

    for line in input_lines:
        [parent, children_list] = line.split(":")
        children = children_list.split()
        if parent in node_map:
            node_map[parent].update(children)
        else:
            node_map[parent] = set(children)

        for child in children:
            if child in node_map:
                node_map[child].add(parent)
            else:
                node_map[child] = set([parent])

    return node_map

def get_result(communities):
    (com1, com2) = communities
    return len(com1) * len(com2)

def get_num_edges_between_communities(node_map, communities):
    num_edges = 0

    (com1, com2) = communities

    for parent in com1:
        for child in node_map[parent]:
            if child in com2:
                num_edges += 1

    print(f"Num Edges: {num_edges}")

    return num_edges

# Karger's algorithm for calculating a minimum cut to separte clusters / communities
def solve(node_map):
    for _ in range(100):
        communities = get_communities_karger(copy.deepcopy(node_map))
        if get_num_edges_between_communities(node_map, communities) == 3:
            return get_result(communities)

    # for parent, children in node_map.items():
    #     print(f"{parent} has {len(children)} children.")

    return 0


def get_communities_karger(node_map):
    while len(node_map) > 2:
         parent = random.choice(list(node_map.keys()))
         child = random.choice(list(node_map[parent]))
         #print(f'Merging {parent} <==> {child}...')
         merge_nodes(node_map, parent, child)

    communities = list(node_map.keys())
    com1 = communities[0].split("_")
    com2 = communities[1].split("_")
    return (com1, com2)

def merge_nodes(node_map, parent, child):
    children = node_map[parent]
    children.remove(child)
    grandchildren = node_map[child]
    grandchildren.remove(parent)

    merged_node = parent + "_" + child
    node_map[merged_node] = children.union(grandchildren)
    del node_map[parent]
    del node_map[child]

    for sibling in children:
        node_map[sibling].remove(parent)
        node_map[sibling].add(merged_node)
    
    for grandchild in grandchildren:
        node_map[grandchild].remove(child)
        node_map[grandchild].add(merged_node)

    #print(node_map)

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    print(initial_state)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2023
DAY = 25

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 54
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
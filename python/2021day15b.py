#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def parse_input(input):
    nodes = {}

    x = 0
    for line in input:
        y = 0
        for char in line:
            nodes[(x, y)] = int(char)
            y += 1
        x += 1

    return nodes, x-1, y-1

def get_neighbours(visited, node, max_x, max_y):

    (x, y) = node
    neighbours = []

    # Diagonal locations do not count
    directions = [(-1, 0), (0, 1), (1,0), (0, -1)]
    for (dx, dy) in directions:
        x1 = x + dx
        y1 = y + dy
        if x1 >= 0 and x1 <= max_x and y1 >= 0 and y1 <= max_y:
            if (x1, y1) not in visited:
                neighbours.append((x1, y1))

    return neighbours


def get_next_node(distance_queue):
    min_distance = min(distance_queue.keys())
    next_node = distance_queue[min_distance][0]
    return next_node

def add(key, dic, item):    
    if key in dic:
        dic[key].append(item)
        #print(f"Added: {item}")
    else:
        dic[key] = [item]
        #print(f"Added: {item}")

def remove(key, dic, item):    
    if key in dic:
        dic[key].remove(item)
        #print(f"Removed: {item}")
        if len(dic[key]) == 0:
            dic.pop(key)

def get_shortest_path(nodes, max_x, max_y):

    width = max_x + 1
    length = max_y + 1

    max_x = width * 5 - 1
    max_y = length * 5 - 1

    distance_queue = {} # 0 : [items at 0 distance away]
    shortest_path = {}
    start = (0, 0)
    end = (max_x, max_y)

    inf = 99999999999999
    # initialize
    
    extra_nodes = {}
    for i in range(0, 5):
        for y in range(length):
            print_string = ""
            for j in range(0, 5):
                for x in range(width):
                    n = (x, y)
                    risk_factor = nodes[n]
                    if i == 0 and j == 0:
                        shortest_path[n] = (inf, None) # (distance_to_node, previous_node)            
                        add(inf, distance_queue, n)
                        print_string += str(risk_factor)
                    else:
                        new_node = (n[0] + i * width, n[1] + j * length)
                        shortest_path[new_node] = (inf, None) # (distance_to_node, previous_node)            
                        add(inf, distance_queue, new_node)
                        additional_risk_factor = i + j    
                        new_risk_factor = (risk_factor + additional_risk_factor) % 10              
                        extra_nodes[new_node] = new_risk_factor
                        print_string += str(new_risk_factor)
            print(print_string)

    nodes.update(extra_nodes)

    shortest_path[start] = (0, None)
    add(0, distance_queue, start)

    visited = []
    more_work_to_do = True
    while more_work_to_do:
        node = get_next_node(distance_queue)
        visited.append(node)
        (distance_to_node, _) = shortest_path[node]
        node_weight = nodes[node]
        remove(distance_to_node, distance_queue, node)
        #print(f"Visiting: {node}")
        neighbours = get_neighbours(visited, node, max_x, max_y)
        for neighbour in neighbours:
            (distance_to_neighbour, _) = shortest_path[neighbour]
            new_distance_to_neighbour = distance_to_node + node_weight
            if new_distance_to_neighbour < distance_to_neighbour:
                #print(f"    found shortest path to {neighbour} : {new_distance_to_neighbour}")
                shortest_path[neighbour] = (new_distance_to_neighbour, node)
                remove(distance_to_neighbour, distance_queue, neighbour)
                # do not add if already visited
                if neighbour not in visited:
                    add(new_distance_to_neighbour, distance_queue, neighbour)
        more_work_to_do = len(visited) < len(nodes)

    (distance_to_end, _) = shortest_path[end]
    distance_to_end -= nodes[start]
    distance_to_end += nodes[end]
    return distance_to_end

def execute(input):
    nodes, max_x, max_y = parse_input(input)    
    shortest_path = get_shortest_path(nodes, max_x, max_y)

    result = shortest_path
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 15

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test_super_small")
input = get_strings(raw_input)
assert execute(input) == 136 # no idea if this is correct or not
print("TEST INPUT (super small) PASSED")

raw_input = get_input(YEAR, DAY, "_test_small")
input = get_strings(raw_input)
assert execute(input) == 171 # no idea if this is correct or not
print("TEST INPUT (small) PASSED")

raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 315 # not 261
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 707
print("ANSWER CORRECT")
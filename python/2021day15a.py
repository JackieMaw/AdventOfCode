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

    #for i in range(max(x-1, 0), min(x+2, max_x)):
        #for j in range(max(y-1, 0), min(y+2, max_y)):
            #if not (i == x and j == y):

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

    # next_node = None
    # distance_to_next_node = None
    # for (node, (distance, _)) in shortest_path.items():
    #     if node not in visited:
    #         if next_node is None: # we have no value yet so pick the first one
    #             next_node = node
    #             distance_to_next_node = distance
    #         elif distance is not None: # we found something with a valid distance
    #             if distance_to_next_node is None or distance < distance_to_next_node:
    #                 next_node = node
    #                 distance_to_next_node = distance
    # return next_node

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

    distance_queue = {} # 0 : [items at 0 distance away]
    shortest_path = {}
    start = (0, 0)
    end = (max_x, max_y)

    inf = 99999999999999
    # initialize
    shortest_path[start] = (0, None)
    add(0, distance_queue, start)
    for n in nodes:
        if n != start:
            shortest_path[n] = (inf, None) # (distance_to_node, previous_node)            
            add(inf, distance_queue, n)

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
raw_input = get_input(YEAR, DAY, "_test_small")
input = get_strings(raw_input)
assert execute(input) == 12
print("TEST INPUT (small) PASSED")

raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 40
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0 #711 is wrong :-(
print("ANSWER CORRECT")
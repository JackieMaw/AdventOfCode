#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy
import heapq

def get_risk_factors(input_data):

    width = len(input_data[0])
    length = len(input_data)

    total_width = width * 5
    total_length = length * 5
    risk_factors = [ [ 0 for i in range(total_width) ] for j in range(total_length) ]

    for x in range(width):
        for y in range(length):

            risk_factor = int(input_data[y][x])

            for j in range(0, 5):
                for i in range(0, 5):

                    if i == 0 and j == 0:
                        risk_factors[y][x] = risk_factor

                    else:
                        new_x = x + i * width
                        new_y = y + j * length
                        additional_risk_factor = i + j    
                        new_risk_factor = (risk_factor + additional_risk_factor)
                        if new_risk_factor > 9:
                            new_risk_factor -= 9            
                        risk_factors[new_y][new_x] = new_risk_factor

    #display_matrix(risk_factors)

    return risk_factors, total_width, total_length

def get_neighbours(visited, node, max_x, max_y):

    (x, y) = node
    neighbours = []

    # Diagonal locations do not count
    directions = [(-1, 0), (0, 1), (1,0), (0, -1)]
    for (dx, dy) in directions:
        x1 = x + dx
        y1 = y + dy
        if x1 >= 0 and x1 < max_x and y1 >= 0 and y1 < max_y:
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

def display_matrix(matrix):
    for row in matrix:
        print(' '.join([ str(col) for col in row ]))

def get_shortest_path(risk_factors, total_width, total_length):

    shortest_path = [ [ None for _ in range(total_width) ] for _ in range(total_length) ]
    visited = [ [ 0 for _ in range(total_width) ] for _ in range(total_length) ]

    priority_queue = [(0, 0, 0)] # (cost, x, y)
    shortest_path[0][0] = 0

    #display_matrix(shortest_path)
    #display_matrix(visited)

    while len(priority_queue) > 0:
        (distance_to_node, x, y) = heapq.heappop(priority_queue)
        visited[y][x] = 1
        node_weight = risk_factors[y][x]
        #print(f"Visiting: {(x, y)}")
        neighbours = get_neighbours(visited, (x, y), total_width, total_length)
        for (nx, ny) in neighbours:
            distance_to_neighbour = shortest_path[ny][nx]
            new_distance_to_neighbour = distance_to_node + node_weight
            if distance_to_neighbour is None or new_distance_to_neighbour < distance_to_neighbour:
                #print(f"    found shortest path to {(nx, ny)} : {new_distance_to_neighbour}")
                shortest_path[ny][nx] = new_distance_to_neighbour
                # do not add if already visited
                if not visited[ny][nx]:
                    heapq.heappush(priority_queue, (new_distance_to_neighbour, nx, ny))

    distance_to_end = shortest_path[total_length - 1][total_width - 1]
    distance_to_end -= risk_factors[0][0]
    distance_to_end += risk_factors[total_length - 1][total_width - 1]
    return distance_to_end

def execute(input_data):
    risk_factors, total_width, total_length = get_risk_factors(input_data)    
    shortest_path = get_shortest_path(risk_factors, total_width, total_length)

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
input_data = get_strings(raw_input)
assert execute(input_data) == 136
print("TEST INPUT (super small) PASSED")

raw_input = get_input(YEAR, DAY, "_test_small")
input_data = get_strings(raw_input)
assert execute(input_data) == 204
print("TEST INPUT (small) PASSED")

raw_input = get_input(YEAR, DAY, "_test")
input_data = get_strings(raw_input)
assert execute(input_data) == 315
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_data = get_strings(raw_input)
assert execute(input_data) == 2942
print("ANSWER CORRECT")
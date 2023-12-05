from utilities import *
import math
import copy

class map_item():
    def __init__(self, source, destination, map_range):
        self.source_start = source
        self.destination_offset = destination - source
        self.map_range = map_range
        self.source_end = source + map_range - 1

    def contains(self, number):
        if number >= self.source_start and number <= self.source_end:
            return True
        return False

    def get_destination(self, source):
        return source + self.destination_offset

class map():
    def __init__(self, from_state, to_state, map_items):
        self.from_state = from_state
        self.to_state = to_state
        self.map_items = map_items

def parse_seeds(input_line):
    all_seeds = []
    #"seeds: 79 14 55 13"
    [_, seeds_string] = input_line.split(':')
    seeds = seeds_string.strip().split(' ')
    start = 0
    stop = len(seeds)
    increment_by_two = 2
    for i in range(start, stop, increment_by_two):
        all_seeds.append((int(seeds[i]), int(seeds[i+1])))        
    return all_seeds

def parse_maps(input_lines):
    
    # {"map_name" : map('from_state', 'to_state', [])}
    all_maps = {}
    
    current_map = None
    current_map_items = None

    for line in input_lines:
        if ":" in line: # seed-to-soil map:
            # new map
            [from_state, _, to_state] = line.split(' ')[0].split("-")
            current_map_items = []
            current_map = map(from_state, to_state, current_map_items)
            all_maps[from_state] = current_map
        elif len(line) > 0:
            [destination, source, map_range] = [int(num_string) for num_string in line.strip().split(' ')]
            current_map_items.append(map_item(source, destination, map_range))

    print(all_maps)

    return all_maps

def get_destination_from_map(map, source):
    destination = source
    for map_item in map.map_items:
        if map_item.contains(source):
            destination = map_item.get_destination(source)
    return destination

def execute(input):
    print(input)

    all_seed_ranges = parse_seeds(input[0])
    all_maps = parse_maps(input[2:])

    all_locations = []
    for (range_start, range_length) in all_seed_ranges:

        print(f'RANGE FROM: seed #{range_start} to seed #{range_start + range_length - 1} ==>')

        for seed_number in range(range_start, range_start + range_length):

            #print(f'    seed #{seed_number} >>')
            source = seed_number
            current_state = 'seed'

            while current_state in all_maps:
                map = all_maps[current_state]
                destination = get_destination_from_map(map, source)
                #print(f'        {current_state} number {source} corresponds to {map.to_state} number {destination}.')
                current_state = map.to_state
                source = destination

            all_locations.append(source)

    result = min(all_locations)
    print(f"result: {result}")
    return result

def run_unit_tests():
    assert parse_seeds("seeds: 79 14 55 13") == [(79, 14), (55, 13)]

    all_maps = parse_maps(["seed-to-soil map:", "50 98 2", "52 50 48"])
    assert len(all_maps) == 1
    seed_map = all_maps["seed"]
    assert seed_map.to_state == "soil"
    map_items = seed_map.map_items
    assert len(map_items) == 2
    map = map_items[0]
    assert map.source_start == 98
    assert map.destination_offset == 50 - 98
    assert map.map_range == 2

# TESTS
run_unit_tests()
print("ALL UNIT TESTS PASSED")


YEAR = 2023
DAY = 5

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 46
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 173706076
print("ANSWER CORRECT")
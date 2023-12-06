from utilities import *
import math
import copy

class MapItem():
    def __init__(self, source_start, source_end, destination_start):
        self.source_start = source_start
        self.source_end = source_end
        self.destination_offset = destination_start - source_start

    def contains(self, number):
        if number >= self.source_start and number <= self.source_end:
            return True
        return False    
    
    def is_valid_range(self, range):
        return range[0] <= range[1]
    
    def overlaps_with(self, range_start, range_end):
        out_of_bounds = range_start > self.source_end or range_end < self.source_start
        return not out_of_bounds

    def translate(self, range_start, range_end):

        if range_start >= self.source_start and range_end <= self.source_end:
            return ((range_start + self.destination_offset, range_end + self.destination_offset), []) # no excess

        mapped_range = None
        failed_to_map_ranges = []

        a = range_start
        b = max(self.source_start, range_start)
        c = min(self.source_end, range_end)
        d = range_end

        before_range = (a, b - 1)
        mid_range = (b, c)
        after_range = (c + 1, d)

        #print(f"*** ({range_start}, {range_end}) => ({self.source_start}, {self.source_end}))")
        #print(f"*   {before_range} + {mid_range} + {after_range}")
        
        if self.is_valid_range(mid_range):
            mapped_range = (mid_range[0] + self.destination_offset, mid_range[1] + self.destination_offset) 
            print(f"    {mid_range} ==> {mapped_range}")
                         
        if self.is_valid_range(before_range):
            failed_to_map_ranges.append(before_range)
        
        if self.is_valid_range(after_range):
            failed_to_map_ranges.append(after_range)

        #print(f"*   mapped_range: {mapped_range} failed_to_map_ranges: {failed_to_map_ranges}")
        
        return (mapped_range, failed_to_map_ranges)

    def get_destination(self, source):
        return source + self.destination_offset

class StateMap():
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
        range_start = int(seeds[i])
        range_length = int(seeds[i+1])
        range_end = range_start + range_length - 1
        all_seeds.append((range_start, range_end))
    return all_seeds

def parse_maps(input_lines):
    
    # {"map_name" : StateMap('from_state', 'to_state', [])}
    all_maps = {}
    
    current_map = None
    current_map_items = None

    for line in input_lines:
        if ":" in line: # seed-to-soil map:
            # new map
            [from_state, _, to_state] = line.split(' ')[0].split("-")
            current_map_items = []
            current_map = StateMap(from_state, to_state, current_map_items)
            all_maps[from_state] = current_map
        elif len(line) > 0:
            [destination_start, source_start, map_range] = [int(num_string) for num_string in line.strip().split(' ')]
            source_end = source_start + map_range - 1
            current_map_items.append(MapItem(source_start, source_end, destination_start))

    print(all_maps)

    return all_maps

def get_destination_from_map(state_map, source):
    destination = source
    for map_item in state_map.map_items:
        if map_item.contains(source):
            destination = map_item.get_destination(source)
    return destination

def map_ranges(this_state_map : StateMap, source_ranges):
    
    range_size_before = get_range_size(source_ranges)

    destination_ranges = []
    something_changed = True
    while len(source_ranges) > 0:
        (range_start, range_end) = source_ranges.pop(0)
        something_changed = False
        for map_item in this_state_map.map_items:
            if map_item.overlaps_with(range_start, range_end):
                (mapped_range, failed_to_map_ranges) = map_item.translate(range_start, range_end)
                destination_ranges.append(mapped_range)
                print(f"MAPPING FOUND FOR RANGE : {mapped_range}")
                source_ranges.extend(failed_to_map_ranges)
                something_changed = True
                break
        if not something_changed:
            print(f"NO MAPPING FOR RANGES : {(range_start, range_end)}")
            destination_ranges.append((range_start, range_end))

    range_size_after = get_range_size(destination_ranges)

    assert range_size_before == range_size_after

    return destination_ranges


def get_min_from_ranges(all_ranges):
    return min([start for (start, end) in all_ranges])

def get_range_size(all_ranges):
    return sum([end - start + 1 for (start, end) in all_ranges])

def execute(input):

    print(input)

    all_seed_ranges = parse_seeds(input[0])
    all_maps = parse_maps(input[2:])

    source_ranges = all_seed_ranges
    current_state = 'seed'

    while current_state in all_maps:
        state_map = all_maps[current_state]
        print(f'MAP FROM {state_map.from_state} to {state_map.to_state} : {source_ranges}')
        desintation_ranges = map_ranges(state_map, source_ranges)
        current_state = state_map.to_state
        source_ranges = desintation_ranges

    result = get_min_from_ranges(source_ranges)
    print(f"result: {result}")
    return result

def run_unit_tests():

    assert get_min_from_ranges([(5, 500), (3, 1)]) == 3

    assert MapItem(50, 59, 150).translate(50, 59) == ((150, 159), [])
    assert MapItem(50, 59, 150).translate(60, 69) == (None, [(60, 69)])
    assert MapItem(55, 65, 155).translate(50, 70) == ((155, 165), [(50, 54), (66, 70)])
    assert MapItem(50, 70, 150).translate(55, 65) == ((155, 165), [])

    assert parse_seeds("seeds: 79 14 55 13") == [(79, 92), (55, 67)]

    all_maps = parse_maps(["seed-to-soil map:", "50 98 2", "52 50 48"])
    assert len(all_maps) == 1
    seed_map = all_maps["seed"]
    assert seed_map.to_state == "soil"
    map_items = seed_map.map_items
    assert len(map_items) == 2
    map_range_item2 = map_items[0]
    assert map_range_item2.source_start == 98
    assert map_range_item2.source_end == 99
    assert map_range_item2.destination_offset == 50 - 98

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
assert execute(input) == 11611182
print("ANSWER CORRECT")
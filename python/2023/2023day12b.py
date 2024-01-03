from utilities import *
import math
import copy
from functools import lru_cache
import numpy as np
import itertools

def parse_input(input_lines):
    initial_state = []
    #.#.###.#.###### 1,3,1,6 >>> duplicate 5 times!
    for input_line in input_lines:
        [condition_record, condition_summary_str] = input_line.split()
        condition_record = condition_record + "?" + condition_record + "?" + condition_record + "?" + condition_record + "?" + condition_record
        condition_summary = condition_summary + "," + condition_summary + "," + condition_summary + "," + condition_summary + "," + condition_summary
        initial_state.append((condition_record, condition_summary))
    return initial_state

def solve(initial_state):
    #return sum(get_num_arrangements(condition_record, condition_summary) for (condition_record, condition_summary) in initial_state)
    sum = 0
    for (condition_record, condition_summary) in initial_state:
        print(f">>> {condition_record} {condition_summary} >>>")
        result = get_num_arrangements(condition_record, condition_summary)
        print(f">>> {condition_record} {condition_summary} >>> {result}")
        sum += result
    return sum

def get_summary(chunk):
    return [len(broken_chunk) for broken_chunk in filter(None, chunk.split("."))]

def is_a_match(condition_record_str, condition_summary):
    assert type(condition_record_str) is str
    return get_summary(condition_record_str) == condition_summary

def apply_to_condition_record(condition_record, substring):

    full_string = ""
    substring_index = 0
    for s in condition_record:
        if s == "?":
            full_string += substring[substring_index]
            substring_index += 1
        else:
            full_string += s
    return full_string

def get_all_matching_strings(condition_record, condition_summary):

    print(f"get_all_matching_strings: {condition_record} {condition_summary} >>>")

    if condition_record.count("?") == 0:
        return [condition_record]
    
    num_hashes_expected = sum(condition_summary)
    chunk_hashes = condition_record.count("#")
    need_more_hashes = num_hashes_expected - chunk_hashes

    if need_more_hashes == 0:
        return [condition_record.replace("?", ".")]

    num_dots_expected = len(condition_record) - num_hashes_expected
    chunk_dots = condition_record.count(".")
    need_more_dots = num_dots_expected - chunk_dots

    if need_more_hashes == 0:
        return [condition_record.replace("?", "#")]

    expected_chars = ["#" for _ in range(need_more_hashes)] + ["." for _ in range(need_more_dots)]
    #print(expected_chars)

    all_permutations = set([''.join(perm) for perm in itertools.permutations(expected_chars)])
    #print(all_permutations)

    print(f"    all_permutations: {len(all_permutations)}")

    all_matching_strings = [s for s in [apply_to_condition_record(condition_record, s) for s in all_permutations] if is_a_match(s, condition_summary)]

    print(f"    all_matching_strings: {len(all_matching_strings)}")

    print(f"get_all_matching_strings: {condition_record} {condition_summary} >>> {sorted(all_matching_strings)}")

    return all_matching_strings   

def get_num_arrangements(condition_record, condition_summary):

    #condition_summary = [int(req) for req in condition_summary_str.split(',')]

    product = 1
    for condition_chunk in list(filter(None, condition_record.split('.'))):
        possible_summaries = get_possible_summaries(condition_chunk)
        if len(possible_summaries) == 1:
            print(f"BINGO: condition_chunk {condition_chunk} can only match one summary = {possible_summaries}")
        product *= len(possible_summaries)

    return product

def get_possible_summaries_for_chunk_segments(condition_chunk):
    split_point = len(condition_chunk) // 2
    all_possible_summaries = []

    for s1 in get_possible_summaries(condition_chunk[:split_point]):
        for s2 in get_possible_summaries(condition_chunk[split_point:]):
            all_possible_summaries.append(s1 + s2)

    print(f"______{condition_chunk}______{all_possible_summaries}")

    return list(filter(None, all_possible_summaries))

def get_possible_summaries_for_split_chunks(condition_chunk):
    all_possible_summaries = []

    for split_point in range(1, len(condition_chunk) - 1):
        for s1 in get_possible_summaries(condition_chunk[:split_point]):
            for s2 in get_possible_summaries(condition_chunk[split_point:]):
                all_possible_summaries.append([s1, s2])

    print(f"______{condition_chunk}______{all_possible_summaries}")

    return list(filter(None, all_possible_summaries))

get_possible_summaries_cache = {}
def get_possible_summaries(condition_chunk):
    result = None
    if condition_chunk in get_possible_summaries_cache:
        result = get_possible_summaries_cache[condition_chunk]
    else:
        if condition_chunk.count("?") == 0:
            result = [[condition_chunk.count('#')]]
        elif len(condition_chunk) == 1: # then it must be a ?
            result = [[0], [1]]
        else:
            result = []
            result.append(get_possible_summaries_for_chunk_segments(condition_chunk))
            result.append(get_possible_summaries_for_split_chunks(condition_chunk))
        get_possible_summaries_cache[condition_chunk] = result
    
    print(f"{condition_chunk} >> {result}")

    return result

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS

assert get_all_matching_strings("###", [3]) == ["###"]
assert sorted(get_all_matching_strings("?###????????", [3,2,1])) == ['.###.##.#...', '.###.##..#..', '.###.##...#.', '.###.##....#', '.###..##.#..', '.###..##..#.', '.###..##...#', '.###...##.#.', '.###...##..#', '.###....##.#']

assert get_possible_summaries("###") == [[3]]
assert get_possible_summaries("#?#") == [[2], [3], [1,1]]
assert get_possible_summaries("??#") == [[1, 2, 3]]
assert get_possible_summaries("???") == [[0, 1, 2, 3], [1,1]]
assert get_possible_summaries("?###????????") == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

assert get_num_arrangements("???.###", "1,1,3") == 1
assert get_num_arrangements('??.??.?##', "1,1,3") == 4
assert get_num_arrangements('????.#.#', "4,1,1") == 1
assert get_num_arrangements("???????", "2,1") == 10
assert get_num_arrangements("?###????????", "3,2,1") == 10
print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 12

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 525152
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
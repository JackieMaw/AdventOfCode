from utilities import *
import math
import copy
from functools import lru_cache
import numpy as np

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

def get_num_arrangements(condition_record, condition_summary):

    #condition_summary = [int(req) for req in condition_summary_str.split(',')]

    product = 1
    for condition_chunk in list(filter(None, condition_record.split('.'))):
        possible_summaries = get_possible_summaries(condition_chunk)
        if len(possible_summaries) == 1:
            print(f"BINGO: condition_chunk {condition_chunk} can only match one summary = {possible_summaries}")
        product *= len(possible_summaries)

    return product

get_possible_summaries_cache = {}
def get_possible_summaries(condition_chunk):
    result = None
    if condition_chunk in get_possible_summaries_cache:
        result = get_possible_summaries_cache[condition_chunk]
    else:
        if condition_chunk.count("?") == 0:
            result = [condition_chunk.count('#')]
        elif len(condition_chunk) == 1: # then it must be a ?
            result = [0, 1]
        else:
            split_point = len(condition_chunk) // 2
            all_possible_summaries = set()
            for s1 in get_possible_summaries(condition_chunk[:split_point]):
                for s2 in get_possible_summaries(condition_chunk[split_point:]):
                    all_possible_summaries.add(s1 + s2)
            result = list(all_possible_summaries)
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
assert get_possible_summaries("###") == [3]
assert get_possible_summaries("#?#") == [2, 3]
assert get_possible_summaries("??#") == [1, 2, 3]
assert get_possible_summaries("???") == [0, 1, 2, 3]
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
from utilities import *
import math
import copy
from functools import lru_cache
import numpy as np
import itertools

def parse_input(input_lines):
    initial_state = []
    #.#.###.#.###### 1,3,1,6 x 5
    for input_line in input_lines:
        [condition_record, condition_summary_str] = input_line.split()
        condition_record = condition_record + "?" + condition_record + "?" + condition_record + "?" + condition_record + "?" + condition_record
        condition_record = list(filter(None, condition_record.split('.')))
        condition_summary = [int(req) for req in condition_summary_str.split(',')]
        condition_summary = condition_summary * 5
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

@lru_cache(maxsize=None)
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

def get_all_matching_strings_brute_force(condition_record, condition_summary):

    print(f"get_all_matching_strings_brute_force: {condition_record} {condition_summary} >>>")

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

    print(f"    generating permutations for: {len(expected_chars)} characters")

    all_permutations = list(itertools.permutations(expected_chars))

    print(f"    reducing duplications for: {len(all_permutations)} permutations")

    all_permutations = set([''.join(perm) for perm in all_permutations])
    #print(all_permutations)

    print(f"    all_permutations: {len(all_permutations)}")

    all_matching_strings = [s for s in [apply_to_condition_record(condition_record, s) for s in all_permutations] if is_a_match(s, condition_summary)]

    print(f"    all_matching_strings: {len(all_matching_strings)}")

    print(f"get_all_matching_strings_brute_force: {condition_record} {condition_summary} >>> {sorted(all_matching_strings)}")

    return len(all_matching_strings)

def get_num_arrangements(condition_record_chunks, condition_summary):

    #print(f"get_num_arrangements: {condition_record_chunks} {condition_summary}")

    if len(condition_record_chunks) == 0 or len(condition_summary) == 0:
        assert len(condition_record_chunks) == 0
        assert len(condition_summary) == 0
        return 1

    # before we attempt to brute force    
    # let's see if we can reduce the problem size     

    # SIMPLE REDUCTION: If the number of chunks is the same as the number of conditions
    
    # if len(condition_record_chunks) > 1 and len(condition_record_chunks) == len(condition_summary):
    #     print('BINGO: we have an even split for chunks and conditions')
    #     num_arrangements = 1
    #     for i, chunk in enumerate(condition_record_chunks):
    #         summary = condition_summary[i]
    #         num_arrangements *= get_num_arrangements([chunk], [summary])
    #     return num_arrangements
    
    # COMPLEX REDUCTION: If one of the chunks matches the maximum chunk, then we can eliminate this

    # max_num = max(condition_summary)
    # count_max = condition_summary.count(max_num)

    # if len(condition_record_chunks) > 1 and count_max == 1:
    #     index_of_chunk = None
    #     for i, chunk in enumerate(condition_record_chunks):
    #         if chunk.count("#") == max_num:
    #             print(f'BINGO: chunk #{i} {chunk} meets the largest criteria {max_num}')
    #             index_of_chunk = i
    #             assert len(chunk) == max_num, f"We might be losing something if we dump this chunk: {chunk}"

    #     if index_of_chunk is not None: 
    #         # PROBLEM: we are removing the ENTIRE chunk here even though we might need the rest of it...
    #         # we might need to split the chunk up by putting a dot in front or at the end and then processing the remaining chunk
    #         index_of_max_num = condition_summary.index(max_num)
    #         condition_summary_b4 = condition_summary[:index_of_max_num]
    #         condition_summary_after = condition_summary[index_of_max_num+1:]
    #         chunks_b4 = condition_record_chunks[:index_of_chunk]
    #         chunks_after = condition_record_chunks[index_of_chunk+1:]
    #         return get_num_arrangements(chunks_b4, condition_summary_b4) * get_num_arrangements(chunks_after, condition_summary_after)
    
    return get_all_matching_strings_brute_force('.'.join(condition_record_chunks), condition_summary)

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS
assert get_summary("###") == [3]
assert get_summary("#.#") == [1, 1]
assert get_summary("..#") == [1]
assert get_summary("#..") == [1]
assert get_num_arrangements(["???","###"], [1,1,3]) == 1
assert get_num_arrangements(['??', '??', '?##'], [1,1,3]) == 4
assert get_num_arrangements(['????', '#', '#'], [4, 1, 1]) == 1
assert get_num_arrangements(["?###????????"], [3,2,1]) == 10
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
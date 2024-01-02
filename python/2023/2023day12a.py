from utilities import *
import math
import copy
from functools import lru_cache

def parse_input(input_lines):
    initial_state = []
    #.#.###.#.###### 1,3,1,6
    for input_line in input_lines:
        [condition_record, condition_summary_str] = input_line.split()
        condition_summary = [int(req) for req in condition_summary_str.split(',')]
        initial_state.append((list(filter(None, condition_record.split('.'))), condition_summary))
    return initial_state

def solve(initial_state):
    return sum(get_num_arrangements(condition_record, condition_summary) for (condition_record, condition_summary) in initial_state)

def get_all_possible_strings(condition_record_chunks):

    all_possible_strings = None

    for chunk in condition_record_chunks:
        possible_strings_for_this_chunk = get_all_possible_strings_for_a_single_chunk(chunk)
        if all_possible_strings is None:
            all_possible_strings = possible_strings_for_this_chunk
        else:
            new_all_possible_strings = []
            for first_part in all_possible_strings:
                for next_part in possible_strings_for_this_chunk:
                    new_all_possible_strings.append(first_part + "." + next_part)

    return all_possible_strings

@lru_cache(maxsize=None)
def get_all_possible_strings_for_a_single_chunk(chunk):

    if chunk.count("?") == 0:
        return [chunk]

    if len(chunk) == 1:
        if chunk[0] == "?":
            return [".", "#"]

    all_possible_chunks = []
    for chunk1 in get_all_possible_strings_for_a_single_chunk(chunk[0]):
        for chunk2 in get_all_possible_strings_for_a_single_chunk(chunk[1:]):
            all_possible_chunks.append(chunk1 + chunk2)
    return all_possible_chunks

@lru_cache(maxsize=None)
def get_summary(chunk):
    return [len(broken_chunk) for broken_chunk in filter(None, chunk.split("."))]

def is_a_match(condition_record_str, condition_summary):
    assert type(condition_record_str) is str
    return get_summary(condition_record_str) == condition_summary

def get_num_arrangements_brute_force(condition_record_chunks, condition_summary):

    print(f"get_num_arrangements_brute_force: {condition_record_chunks} {condition_summary}")

    all_possible_strings = get_all_possible_strings(condition_record_chunks)
    num_matching_chunks = sum([is_a_match(s, condition_summary) for s in all_possible_strings])

    return num_matching_chunks

def get_num_arrangements(condition_record_chunks, condition_summary):

    print(f"get_num_arrangements: {condition_record_chunks} {condition_summary}")

    if len(condition_record_chunks) == 0:
        assert len(condition_summary) == 0
        return 1

    max_num = max(condition_summary)
    count_max = condition_summary.count(max_num)

    if len(condition_record_chunks) > 1 and count_max == 1: # let's see if we can simplify this list by identifying the maximum chunk
        index_of_chunk = None
        for i, chunk in enumerate(condition_record_chunks):
            if chunk.count("#") == max_num:
                print(f'BINGO: chunk #{i} {chunk} meets the largest criteria {max_num}')
                index_of_chunk = i

        if index_of_chunk is not None: 
            # PROBLEM: we are removing the ENTIRE chunk here even though we might need the rest of it...
            # we might need to split the chunk up by putting a dot in front or at the end and then processing the remaining chunk
            index_of_max_num = condition_summary.index(max_num)
            condition_summary_b4 = condition_summary[:index_of_max_num]
            condition_summary_after = condition_summary[index_of_max_num+1:]
            chunks_b4 = condition_record_chunks[:index_of_chunk]
            chunks_after = condition_record_chunks[index_of_chunk+1:]
            return get_num_arrangements(chunks_b4, condition_summary_b4) * get_num_arrangements(chunks_after, condition_summary_after)
    
    return get_num_arrangements_brute_force(condition_record_chunks, condition_summary)

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
assert get_all_possible_strings_for_a_single_chunk("???") == ['...', '..#', '.#.', '.##', '#..', '#.#', '##.', '###']
print(get_all_possible_strings(["???","###"]))
assert get_all_possible_strings(["???","###"]) == ['...', '..#', '.#.', '.##', '#..', '#.#', '##.', '###']
assert get_num_arrangements(["???","###"], [1,1,3]) == 1
assert get_num_arrangements(["?###????????"], [3,2,1]) == 10
print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 12

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input_lines = get_strings(raw_input)
assert execute(input_lines) == 21
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
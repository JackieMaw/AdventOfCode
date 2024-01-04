from utilities import *
import math
import copy
from functools import lru_cache
import numpy as np
import itertools
from more_itertools import distinct_permutations

def parse_input(input_lines):
    initial_state = []
    #.#.###.#.###### 1,3,1,6 >>> duplicate 5 times!
    for input_line in input_lines:
        [condition_record, condition_summary] = input_line.split()
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

def get_num_matching_strings_brute_force(condition_record_chunks, condition_summary_chunks):
    return len(get_all_matching_strings_brute_force(condition_record_chunks, condition_summary_chunks))


def get_all_matching_strings_brute_force(condition_record_chunks, condition_summary_chunks):

    condition_record = '.'.join(condition_record_chunks)

    print(f"get_all_matching_strings_brute_force: {condition_record} {condition_summary_chunks} >>>")

    if condition_record.count("?") == 0:
        return [condition_record]
    
    num_hashes_expected = sum(condition_summary_chunks)
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

    all_permutations = list(distinct_permutations(expected_chars))

    #print(f"    reducing duplications for: {len(all_permutations)} permutations")

    #all_permutations = set([''.join(perm) for perm in all_permutations])
    #print(all_permutations)

    print(f"    all_permutations: {len(all_permutations)}")

    all_matching_strings = [s for s in [apply_to_condition_record(condition_record, s) for s in all_permutations] if is_a_match(s, condition_summary_chunks)]

    print(f"    all_matching_strings: {len(all_matching_strings)}")

    print(f"get_all_matching_strings_brute_force: {condition_record} {condition_summary_chunks} >>> {sorted(all_matching_strings)}")

    return all_matching_strings

def get_num_arrangements(condition_record, condition_summary):
    condition_record_chunks = list(filter(None, condition_record.split('.')))
    condition_summary_chunks = [int(s) for s in condition_summary.split(',')]
    return get_num_arrangements_chunks(condition_record_chunks, condition_summary_chunks)

def split_by_max_num(condition_summary_chunks, max_num):
    all_groups_of_chunks = []

    accumulated_chunks = []
    for chunk in condition_summary_chunks:
        if chunk == max_num:
            all_groups_of_chunks.append(accumulated_chunks)
            accumulated_chunks = []
            all_groups_of_chunks.append([chunk]) # add the max as it's own group
        else:
            accumulated_chunks.append(chunk)
    
    if len(accumulated_chunks) > 0:
        all_groups_of_chunks.append(accumulated_chunks)

    return all_groups_of_chunks

def split_by_max_hash(condition_record_chunks, max_num):
    all_groups_of_chunks = []

    accumulated_chunks = []
    for chunk in condition_record_chunks:
        if chunk.count('#') == max_num:
            all_groups_of_chunks.append(accumulated_chunks)
            accumulated_chunks = []

            # what to do with the max chunk?
            # add the max as it's own group
            all_groups_of_chunks.append([chunk]) 
            # surround by dots
            index_of_first_hash = chunk.index("#")
        else:
            accumulated_chunks.append(chunk)
    
    if len(accumulated_chunks) > 0:
        all_groups_of_chunks.append(accumulated_chunks)

    return all_groups_of_chunks


def apply_shortcut(condition_record_chunks, condition_summary_chunks):
    # before doing a brute force, let's check if any chunks are at the maximum hash length
    # or greater than the second maximum
    # these can all be eliminated against the maximum numbers

    max_num = max(condition_summary_chunks)
    count_max_expected = condition_summary_chunks.count(max_num)
    numbers_less_than_max = [c for c in condition_summary_chunks if c < max_num]

    if len(numbers_less_than_max) == 0:
        return None # we cannot apply the shortcut
        
    chunks_with_max_count = [c for c in condition_record_chunks if c.count("#") == max_num]    
    # second_max_num = max(numbers_less_than_max)
    # chunks_with_second_max_count = [c for c in condition_record_chunks if c.count("#") > second_max_num]
    count_max = len(chunks_with_max_count)

    if count_max != count_max_expected:
        return None # we cannot apply the shortcut
    
    print(f'SHORTCUT 1: we can remove all chunks with # count equal to {max_num}')
    # rather than removing the entire chunk, we should replace the chunk with a reduced chunk
    # ?###???????? >> .###.??????? >> ??????? TOO COMPLICATED
    # we can also split the chunks up
    
    split_condition_record_chunks = split_by_max_hash(condition_record_chunks, max_num)
    split_condition_summary_chunks = split_by_max_num(condition_summary_chunks, max_num)

    zipped_chunks = list(zip(split_condition_record_chunks, split_condition_summary_chunks))

    result = np.prod([get_num_arrangements_chunks(condition_record_chunks, condition_summary_chunks) for [condition_record_chunks, condition_summary_chunks] in zipped_chunks])

    return result

def get_num_arrangements_chunks(condition_record_chunks, condition_summary_chunks):

    print(f"get_num_arrangements_chunks: {condition_record_chunks} {condition_summary_chunks} >>>")

    result = apply_shortcut(condition_record_chunks, condition_summary_chunks)

    if result is None:
        result = get_num_matching_strings_brute_force(condition_record_chunks, condition_summary_chunks)
    
    print(f"get_num_arrangements_chunks: {condition_record_chunks} {condition_summary_chunks} >>> {result}")

    return result

def execute(input_lines):
    print(input_lines)
    initial_state = parse_input(input_lines)
    result = solve(initial_state)
    print(f"result: {result}")
    return result

# TESTS
assert get_all_matching_strings_brute_force(["###"], [3]) == ["###"]
assert sorted(get_all_matching_strings_brute_force(["?###????????"], [3,2,1])) == ['.###.##.#...', '.###.##..#..', '.###.##...#.', '.###.##....#', '.###..##.#..', '.###..##..#.', '.###..##...#', '.###...##.#.', '.###...##..#', '.###....##.#']

assert get_num_arrangements("???.###", "1,1,3") == 1
assert get_num_arrangements('??.??.?##', "1,1,3") == 4
assert get_num_arrangements('????.#.#', "4,1,1") == 1
assert get_num_arrangements("???????", "2,1") == 10
assert get_num_arrangements("???????", "0") == 1
assert get_num_arrangements("????????###????????", "3,2,1") == 10
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
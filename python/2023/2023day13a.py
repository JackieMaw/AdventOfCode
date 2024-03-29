from utilities import *
import math
import copy

def parse_input(input_lines):
    chunks = []

    this_chunk = []
    for input_line in input_lines:
        if input_line == "":
            chunks.append(this_chunk)
            this_chunk = []
        else:
            this_chunk.append(input_line)
    
    chunks.append(this_chunk)
    return chunks

def is_row_fold_at(row_fold, chunk):

    for offset in range(1, row_fold + 1): # this boundary is wrong
        row_before = row_fold - offset
        row_after = row_fold - 1 + offset
        if row_before >= 0 and row_after < len(chunk):
            if chunk[row_before] != chunk[row_after]:
                return False
    
    return True

def is_col_fold_at(col_fold, chunk):

    for offset in range(1, col_fold + 1): # this boundary is wrong
        col_before = col_fold - offset
        col_after = col_fold - 1 + offset
        if col_before >= 0 and col_after < len(chunk[0]):
            for row in chunk:
                if row[col_before] != row[col_after]:
                    return False
    
    return True

def get_reflection_value(chunk):

    for row_fold in range(1, len(chunk)):
        if is_row_fold_at(row_fold, chunk):
            return row_fold * 100

    for col_fold in range(1, len(chunk[0])):
        if is_col_fold_at(col_fold, chunk):
            return col_fold

    raise Exception("Unexpected case: No Fold")

def get_total_reflection_value(chunks):
    total_value = 0
    for chunk in chunks:
        total_value += get_reflection_value(chunk)
    return total_value

def execute(input_lines):
    print(input_lines)
    chunks = parse_input(input_lines)
    result = get_total_reflection_value(chunks)
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 13

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert execute(input) == 5
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 400
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 405
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 35691
print("ANSWER CORRECT")
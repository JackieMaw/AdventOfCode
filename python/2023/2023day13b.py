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

def check_row_fold_at(row_fold, chunk):

    num_differences = 0
    num_rows = len(chunk)
    num_cols = len(chunk[0])
    #print(f"row_fold {row_fold} - checking from offset 1 to {min(row_fold, num_rows - row_fold)}")
    for offset in range(1, min(row_fold, num_rows - row_fold) + 1):
        row_before = row_fold - offset
        row_after = row_fold - 1 + offset
        if row_before >= 0 and row_after < num_rows:
            for col_number in range(num_cols):
                if chunk[row_before][col_number] != chunk[row_after][col_number]:
                    num_differences += 1
    
    return num_differences

def check_col_fold_at(col_fold, chunk):

    num_differences = 0
    num_cols = len(chunk[0])
    #print(f"col_fold {col_fold} - checking from offset 1 to {min(col_fold, num_cols - col_fold)}")
    for offset in range(1, min(col_fold, num_cols - col_fold) + 1):
        col_before = col_fold - offset
        col_after = col_fold - 1 + offset
        if col_before >= 0 and col_after < num_cols:
            for row in chunk:
                if row[col_before] != row[col_after]:
                    num_differences += 1
    
    return num_differences

def get_reflection_value(chunk):

    for row_fold in range(1, len(chunk)):
        if check_row_fold_at(row_fold, chunk) == 1:
            return row_fold * 100

    for col_fold in range(1, len(chunk[0])):
        if check_col_fold_at(col_fold, chunk) == 1:
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
assert execute(input) == 300
raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 100
raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert execute(input) == 400
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings(raw_input)
assert execute(input_lines) == 39037
print("ANSWER CORRECT")
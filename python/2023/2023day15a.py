from utilities import *
import math
import copy

def get_hash(text):
    current_value = 0
    for c in text:
        assert ord(c) is not 10
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value

def get_sum_of_hashes(all_text):
    return sum(get_hash(text) for text in all_text)

def execute(all_text):
    print(all_text)
    result = get_sum_of_hashes(all_text)
    print(f"result: {result}")
    return result

# TESTS
assert get_hash("HASH") == 52
assert execute("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")) == 1320
print("UNIT TESTS PASSED")

YEAR = 2023
DAY = 15

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings_csv(raw_input)
assert execute(input_lines) == 0
print("ANSWER CORRECT")
from utilities import *
import math
import copy

def is_symbol(char):
    if char.isdigit():
        return False
    elif char == '.':
        return False
    else:
        return True

def is_adjacent_to_symbol(all_lines, row, col):
    adjacency = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]

    for (r, c) in adjacency:
        if row + r >= 0 and row + r < len(all_lines):
            if col + c >= 0 and col + c < len(all_lines[0]):
                if is_symbol(all_lines[row + r][col + c]):
                    return True
 
    return False

def execute(all_lines):
    print(all_lines)
    result = 0

    all_part_numbers = []

    all_digits = ''
    is_part_number = False

    for row, line in enumerate(all_lines):
        for col, char in enumerate(line):
            if char.isdigit():
                all_digits += char
                if not is_part_number:
                    if is_adjacent_to_symbol(all_lines, row, col):
                        is_part_number = True
            else: # it's not a digit
                if len(all_digits) > 0: #reset
                    if is_part_number:  #save the last part_number
                        all_part_numbers.append(int(all_digits))
                        print(f"Part Number Found: {all_digits}")
                        is_part_number = False #reset
                    all_digits = '' #reset

        # don't forget to save the last number on each line!
        if len(all_digits) > 0 and is_part_number:
            all_part_numbers.append(int(all_digits))
            print(f"Part Number Found @ EOL: {all_digits}")

    result = sum(all_part_numbers)
    print(f"result: {result}")
    return result

# TESTS
assert is_adjacent_to_symbol(["868*10"], 0, 2) == True
assert is_adjacent_to_symbol(["868*10"], 0, 4) == True
assert execute(["868*10"]) == 878
print("ALL TESTS PASSED")

YEAR = 2023
DAY = 3

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 4361

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert execute(input) == 6288
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
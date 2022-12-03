from utilities import *
import math
import copy

def get_priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:        
        return ord(item) - ord('A') + 27

def split_compartments(rucksack):
    half = int(len(rucksack)/2)
    compartment1 = rucksack[0:half]
    compartment2 = rucksack[half:]
    return (compartment1, compartment2)

def chunks(compartments, n):
    for i in range(0, len(compartments), n):
        yield compartments[i:i + n]

def execute(input):
    priority_sum = 0
    for elf_group in chunks(input, 3):
        common_item = set(elf_group[0]).intersection(elf_group[1]).intersection(elf_group[2]).pop()
        print(common_item)
        priority_sum += get_priority(common_item)
    result = priority_sum
    print(f"result: {result}") 
    return result

# TESTS
assert split_compartments('vJrwpWtwJgWrhcsFMMfFFhFp') == ('vJrwpWtwJgWr','hcsFMMfFFhFp')
assert get_priority('A') == 27
assert get_priority('Z') == 52
assert get_priority('a') == 1
assert get_priority('z') == 26
print("ALL TESTS PASSED")

YEAR = 2022
DAY = 3

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 7826
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def get_frequencies(input):
    size = len(input[0])
    m = []
    for i in range(0,size):
            pos_list = []
            for j in range(0,2):
                pos_list.append(0)
            m.append(pos_list)
    for num in input:
        nums = [char for char in num]
        for i in range(0,size):
            n = int(nums[i])
            m[i][n] += 1
    return m

def get_commons(input):
    size = len(input[0])

    m = get_frequencies(input)
    
    most_common_digits = ""
    least_common_digits = ""
    for i in range(0,size):

        num_occurances_for_ith_bit = m[i]
        most_common_digit = 1
        least_common_digit = 0

        # edge case: if all the frequencies are the same, the least common digit the same as the most common digit       
        # also, a frequency of 0 is not counted    

        all_same = True
        first_frequency = num_occurances_for_ith_bit[0]
        for j in range(1,2):
            if num_occurances_for_ith_bit[j] != first_frequency:
                all_same = False

        if not all_same:
            max_frequency = 0
            min_frequency = 99999999
            for j in range(0,2):
                frequency = num_occurances_for_ith_bit[j]
                if frequency > max_frequency:
                    max_frequency = frequency
                    most_common_digit = j
                if frequency> 0 and frequency < min_frequency:
                    min_frequency = frequency
                    least_common_digit = j
                
        most_common_digits += str(most_common_digit)
        least_common_digits += str(least_common_digit)  

    return (most_common_digits, least_common_digits)

def execute(input):
    (gamma, epsilon) = get_commons(input)
    print(f"gamma: {gamma} => {int(gamma, 2)}")
    print(f"epsilon: {epsilon} => {int(epsilon, 2)}")   
    result = int(gamma, 2) * int(epsilon, 2) 
    print(f"result: {result}") 
    return result

#############################################################

YEAR = 2021
DAY = 3

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 198
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 2724524
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *


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

    size = len(input[0])

    o2 = input.copy()
    (gamma, epsilon) = get_commons(o2)
    #print(o2)
    for i in range(0,size):
        o2 = [item for item in o2 if gamma[i] == item[i]]
        #print(f"{i}: o2 has {len(o2)} options left")
        #print(o2)
        if len(o2) == 1:
            break
        (gamma, epsilon) = get_commons(o2)

    co2 = input.copy()
    (gamma, epsilon) = get_commons(co2)
    for i in range(0,size):
        co2 = [item for item in co2 if epsilon[i] == item[i]]
        #print(f"{i}: co2 has {len(co2)} options left")
        #print(co2)
        if len(co2) == 1:
            break
        (gamma, epsilon) = get_commons(co2)

    print(f"o2: {o2[0]} => {int(o2[0], 2)}")
    print(f"co2: {co2[0]} => {int(co2[0], 2)}")
    result = int(o2[0], 2) * int(co2[0], 2)
    print(f"result: {result}") 
    return result

# TESTS
assert ('1', '1') == get_commons(['1', '1'])
assert ('0', '0') == get_commons(['0', '0'])
assert ('1', '0') == get_commons(['1', '0'])
assert ('1', '0') == get_commons(['0', '1'])
assert ('000001001111', '000001001100') == get_commons(['000001001100', '000001001111'])
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 3

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 230
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 2775870
print("ANSWER CORRECT")
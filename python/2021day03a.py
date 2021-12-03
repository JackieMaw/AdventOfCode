#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):

    size = 12
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
    print(m)

    gamma = ""
    epsilon = ""
    for i in range(0,size):

        pos_list = m[i]
        max_gamma = 0
        i_gamma = 0
        min_epsilon = 99999999
        i_epsilon = 0

        for j in range(0,2):
            if pos_list[j] > max_gamma:
                max_gamma = pos_list[j]
                i_gamma = j
            if pos_list[j] < min_epsilon:
                min_epsilon = pos_list[j]
                i_epsilon = j
        
        gamma += str(i_gamma)
        epsilon += str(i_epsilon)


    print(gamma)
    print(epsilon)

    return int(gamma, 2) * int(epsilon, 2) 

# TESTS
# assert execute(get_strings(["ABCD"])) == 0
# print("ALL TESTS PASSED")

# REAL INPUT DATA
YEAR = 2021
DAY = 3
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
print(execute(input))
# assert execute(input) == 0
# print("ANSWER CORRECT")
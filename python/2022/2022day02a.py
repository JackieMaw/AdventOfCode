from utilities import *
import math
import copy

their_score = {'A': 1, 'B': 2, 'C': 3}
our_score = {'X': 1, 'Y': 2, 'Z': 3}

we_win = [(3,1), (2,3), (1,2)]

def get_score(round):
    them = their_score[round[0]]
    us = our_score[round[2]]
    if them == us:
        # it's a draw
        return 3 + us
    elif (them, us) in we_win:
        # we won
        return 6 + us
    else:
        # they won
        return 0 + us

def execute(input):
    total_score = 0
    for round in input:
        total_score += get_score(round)
    result = total_score
    print(f"result: {result}") 
    return result

# TESTS
assert execute(['A Y', 'B X', 'C Z']) == 15
print("ALL TESTS PASSED")

YEAR = 2022
DAY = 2

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 11906
print("ANSWER CORRECT")
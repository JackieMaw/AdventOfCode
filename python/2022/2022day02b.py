from utilities import *
import math
import copy

their_score = {'A': 1, 'B': 2, 'C': 3}
our_score = {'X': 1, 'Y': 2, 'Z': 3}

to_win = {3:1, 2:3, 1:2}
to_lose = {1:3, 3:2, 2:1}

def get_score(round):
    them = their_score[round[0]]
    outcome = round[2]
    if outcome == 'X': # we should lose
        us = to_lose[them]
        return 0 + us
    elif outcome == 'Y': # we should draw
        us = them
        return 3 + us
    elif outcome == 'Z': # we should win
        us = to_win[them]
        return 6 + us

def execute(input):
    print(input)

    total_score = 0
    for round in input:
        total_score += get_score(round)
    result = total_score
    print(f"result: {result}") 
    return result

# TESTS
assert execute(['A Y', 'B X', 'C Z']) == 12
print("ALL TESTS PASSED")

YEAR = 2022
DAY = 2

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 11906
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(p1_position, p2_position):

    # our board is from 0 to 9
    p1_position -= 1
    p2_position -= 1

    dice_rounds = 0
    dice = 0
    p1_score = 0
    p2_score = 0
    p1_turn = True
    while p1_score < 1000 and p2_score < 1000:
        # roll 1
        dice += 1
        forward = dice
        rolls = f"{dice}"
        if dice > 100:
            dice -= 100
            dice_rounds += 1
        # roll 2
        dice += 1
        forward += dice
        rolls += f"+{dice}"
        if dice > 100:
            dice -= 100
            dice_rounds += 1
        # roll 3
        dice += 1
        forward += dice
        rolls += f"+{dice}"
        if dice > 100:
            dice -= 100
            dice_rounds += 1
        if p1_turn:
            p1_position += forward
            p1_position = p1_position % 10
            p1_score += p1_position + 1
            print(f"Player 1 rolls {rolls} and moves to space {p1_position + 1} for a total score of {p1_score}. Rolls = {(dice_rounds * 100 + dice)}")
            p1_turn = False
        else:
            p2_position += forward
            p2_position = p2_position % 10
            p2_score += p2_position + 1
            print(f"Player 2 rolls {rolls} and moves to space {p2_position + 1} for a total score of {p2_score}. Rolls = {(dice_rounds * 100 + dice)}")
            p1_turn = True

    print(input)
    result = (dice_rounds * 100 + dice) * min(p1_score, p2_score)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 21

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
assert execute(4, 8) == 739785
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
assert execute(6, 7) == 921585
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl, stat
from utilities import *
import math
import copy

def move(state, forward): # this is for one roll, we need to do three rolls, also when does someone win

    (p1_turn, (p1_position, p1_score), (p2_position, p2_score)) = state

    if p1_turn:
        p1_position += forward
        p1_position = p1_position % 10
        p1_score += p1_position + 1        
        p1_turn = False
    else:
        p2_position += forward
        p2_position = p2_position % 10
        p2_score += p2_position + 1        
        p1_turn = True

    new_state = (p1_turn, (p1_position, p1_score), (p2_position, p2_score))
    return new_state

def play(state, dice_moves):
    new_states = {}

    for forward, num in dice_moves.items():
        new_state = move(state, forward)
        if new_state in new_states:
            new_states[new_state] += num
        else:
            new_states[new_state] = num

    return new_states

def get_dice_moves():

    dice_moves = {}
    for d1 in range (1, 4):
        for d2 in range (1, 4):
            for d3 in range (1, 4):
                forward = d1 + d2 + d3
                if forward in dice_moves:
                    dice_moves[forward] += 1
                else:
                    dice_moves[forward] = 1
    return dice_moves                 

def execute(p1_starting_osition, p2_starting_position):

    # our board is from 0 to 9
    p1_starting_osition -= 1
    p2_starting_position -= 1

    p1_won = 0
    p2_won = 0

    # states = {state : number of occurances}
    # state = (p1_turn, (p1_position, p1_score), (p2_position, p2_score))
    start_state = (True, (p1_starting_osition, 0), (p2_starting_position, 0))
    states = { start_state : 1 }

    dice_moves = get_dice_moves()
    
    while len(states) > 0:
        all_new_states = {}

        for state, num in states.items():
            new_states = play(state, dice_moves)
            for new_state, new_num in new_states.items():
                (p1_turn, (p1_position, p1_score), (p2_position, p2_score)) = new_state
                if p1_score >= 21:
                    p1_won += num * new_num
                elif p2_score >= 21:
                    p2_won += num * new_num
                else:
                    if new_state in all_new_states:
                        all_new_states[new_state] += num * new_num
                    else:
                        all_new_states[new_state] = num * new_num

        states = all_new_states    

    print(input)
    result = max(p1_won, p2_won)
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
assert execute(4, 8) == 444356092776315
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
assert execute(6, 7) == 911090395997650
print("ANSWER CORRECT")
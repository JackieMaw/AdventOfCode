from collections import defaultdict
from utilities import *
import math
import copy

def get_max_colours(line):

    max_per_colour = defaultdict(int)

    game_info = line.split(':')
    game_id = int(game_info[0].split(' ')[1])
    games = game_info[1].split(';')
    for game in games:
        colours = game.split(',')
        for colour in colours:
            play = colour.strip().split(' ')
            num = play[0]
            colour = play[1]
            this_max = int(num)
            if this_max > max_per_colour[colour]:
                max_per_colour[colour] = this_max

    print(f"{game_id} =>  {max_per_colour}")
    return (game_id, max_per_colour)

def is_possible(max_colours, goal):
    for colour, max_blocks_allowed in goal.items():
        if max_colours[colour] > max_blocks_allowed:
            return False
    return True

def execute(input):
    print(input)
    result = 0

    goal = {'blue': 14, 'red': 12, 'green': 13}

    for line in input:
        (game_id, max_per_colour) = get_max_colours(line)
        if is_possible(max_per_colour, goal):
            result += game_id

    print(f"result: {result}")
    return result

# TESTS
assert get_max_colours("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == (1, {'blue': 6, 'red': 4, 'green': 2})
assert get_max_colours("Game 71: 1 red, 2 blue, 9 green; 3 red, 8 green; 1 red, 2 blue, 6 green; 3 red, 6 blue, 8 green; 6 green, 3 blue, 2 red; 3 red, 8 green, 6 blue") == (71, {'red': 3, 'blue': 6, 'green': 9})
print("ALL TESTS PASSED")

YEAR = 2023
DAY = 2

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 8
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 2683
print("ANSWER CORRECT")
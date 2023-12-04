import numpy
from utilities import *

def get_points(all_numbers):
    
    (winning_numbers, my_numbers) = all_numbers
    points = 0

    num_wins = len(numpy.intersect1d(winning_numbers, my_numbers))

    if num_wins > 0:
        points = 2 ** (num_wins - 1)

    print (f"{num_wins} matches ==> {points} points")
    return points

def parse_line(line):
    game_info = line.split(':')
    #card_id = int(game_info[0].split(' ')[1])
    [winning_numbers, my_numbers] = game_info[1].split('|')
    return (winning_numbers.strip().split(), my_numbers.strip().split())

def execute(input):
    print(input)
    result = 0

    for line in input:
        result += get_points(parse_line(line))

    print(f"result: {result}")
    return result

# TESTS
assert get_points(parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")) == 8

YEAR = 2023
DAY = 4

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 13
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 25004
print("ANSWER CORRECT")
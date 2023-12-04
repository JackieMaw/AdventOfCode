import numpy
from utilities import *

def get_matching_numbers(all_numbers):
    
    (winning_numbers, my_numbers) = all_numbers
    points = 0

    num_wins = len(numpy.intersect1d(winning_numbers, my_numbers))
    return num_wins

def parse_line(line):
    game_info = line.split(':')
    #card_id = int(game_info[0].split(' ')[1])
    [winning_numbers, my_numbers] = game_info[1].split('|')
    return (winning_numbers.strip().split(), my_numbers.strip().split())

def execute(input):
    print(input)
    result = 0

    #card = [card_count, points]
    # we start off with one of each card
    all_cards = [[1, get_matching_numbers(parse_line(line))] for line in input]

    for card_num in range(len(all_cards)):
        [card_count, points] = all_cards[card_num]
        print(f"{card_count} x Card #{card_num + 1} has {points} matching numbers")
        for p in range(1, points + 1):
            all_cards[card_num + p][0] += card_count
            print(f"{card_count} extra copies => {all_cards[card_num + p][0]} x Card #{card_num + 1 + p}")

    result = sum([card[0] for card in all_cards])
    print(f"result: {result}")
    return result

# TESTS
assert get_matching_numbers(parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")) == 4

YEAR = 2023
DAY = 4

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 30
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 14427616
print("ANSWER CORRECT")
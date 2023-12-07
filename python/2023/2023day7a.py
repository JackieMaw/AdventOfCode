import collections
from utilities import *
import math
import copy
from enum import Enum

ht_5ofaKind = '7_5ofaKind___'
ht_4ofaKind = '6_4ofaKind___'
ht_FullHouse  = '5_FullHouse__'
ht_3ofaKind = '4_3ofaKind___'
ht_TwoPair = '3_TwoPair____'
ht_OnePair = '2_OnePair____'
ht_HighCard = '1_HighCard___'

#card_strength_map = {'A':'E', 'K':'D', 'Q':'C', 'J':'B', 'T':'A'}
#hand_type = Enum('HandType', ['7_5ofaKind___', '6_4ofaKind___', '5_FullHouse__', '4_3ofaKind___', '3_TwoPair____', '2_OnePair____', '1_HighCard'])

def get_hand_type(hand_string):
    counter = collections.Counter(hand_string)
    print(f'{hand_string} => {counter}')

    max_num = max(counter.values())

    if max_num == 1:
        return ht_HighCard
    elif max_num == 2:
        num_pairs = collections.Counter(counter.values())[2]
        if num_pairs == 1:
            return ht_OnePair
        else:
            return ht_TwoPair
    elif max_num == 3:
        num_pairs = collections.Counter(counter.values())[2]
        if num_pairs == 0:
            return ht_3ofaKind
        else:
            return ht_FullHouse
    elif max_num == 4:
        return ht_4ofaKind
    elif max_num == 5:
        return ht_5ofaKind
    else:
        raise Exception(f'Unexpected case: max_num {max_num}')

    #for char, count in counter.items()

def get_sortable_string(hand_string):
    return hand_string.replace('A','E').replace('K','D').replace('Q','C').replace('J','B').replace('T','A')

def get_sortable_hand(hand_string):
    return get_hand_type(hand_string) + get_sortable_string(hand_string)

def get_key(list_item):
    [hand_string, bid] = list_item
    return hand_string

def get_ranked_hands(input):
    # embedded list comprehensions... not good
    sortable_hands = [[get_sortable_hand(hand_string), int(bid)] for [hand_string, bid] in [input_line.split() for input_line in input]]
    sortable_hands.sort(key=get_key)
    return sortable_hands

def execute(input):
    print(input)
    result = 0
    
    #[(hand, bid, rank), ()]
    ranked_hands = get_ranked_hands(input)

    for index, [hand, bid] in enumerate(ranked_hands):
        result += bid * (index + 1)

    print(f"result: {result}")
    return result

# TESTS
assert get_hand_type('AAAAA') == ht_5ofaKind
assert get_hand_type('5AAAA') == ht_4ofaKind
assert get_hand_type('55444') == ht_FullHouse
assert get_hand_type('55543') == ht_3ofaKind
assert get_hand_type('55443') == ht_TwoPair
assert get_hand_type('54322') == ht_OnePair
assert get_hand_type('54321') == ht_HighCard
assert get_sortable_hand('54321') == ht_HighCard + '54321'
assert get_sortable_hand('AKQJT') == ht_HighCard + 'EDCBA'
print("ALL TESTS PASSED")

YEAR = 2023
DAY = 7

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 6440
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 253866470
print("ANSWER CORRECT")
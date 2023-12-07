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
    

    string_without_jokers = hand_string.replace('J', '')

    num_jokers = 5 - len(string_without_jokers)
    counter = collections.Counter(string_without_jokers)
    if num_jokers < 5:
        max_count_without_jokers = max(counter.values())
    else:
        max_count_without_jokers = 0
    max_count = max_count_without_jokers + num_jokers
    
    print(f'{hand_string} => {counter} plus {num_jokers} jokers')

    if max_count == 1:
        return ht_HighCard
    elif max_count == 2:
        num_pairs_without_the_jokers = collections.Counter(counter.values())[2]
        if num_pairs_without_the_jokers == 0 and num_jokers > 0:
            return ht_OnePair
        elif num_pairs_without_the_jokers == 1:
            if num_jokers == 0:
                return ht_OnePair
            else:
                return ht_TwoPair
        elif num_pairs_without_the_jokers == 2:
            return ht_TwoPair
        else:
            raise Exception(f"Unexpected case num_pairs: {num_pairs_without_the_jokers}")
    elif max_count == 3:
        num_pairs_without_the_jokers = collections.Counter(counter.values())[2]
        if num_pairs_without_the_jokers == 0:
            return ht_3ofaKind
        elif num_pairs_without_the_jokers == 1:
            if num_jokers == 0:
                return ht_FullHouse
            else:            
                return ht_3ofaKind
        elif num_pairs_without_the_jokers == 2:
            return ht_FullHouse
        else:
            raise Exception(f"Unexpected case num_pairs: {num_num_pairs_without_the_jokers}")
    elif max_count == 4:
        return ht_4ofaKind
    elif max_count >= 5:
        return ht_5ofaKind
    else:
        raise Exception(f'Unexpected case: max_num {max_count}')

    #for char, count in counter.items()

def get_sortable_string(hand_string):
    return hand_string.replace('A','E').replace('K','D').replace('Q','C').replace('J','0').replace('T','A')

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
assert get_hand_type('JJJJJ') == ht_5ofaKind
assert get_hand_type('JJJJA') == ht_5ofaKind
assert get_hand_type('JJJAB') == ht_4ofaKind
assert get_hand_type('JJJAA') == ht_5ofaKind
assert get_hand_type('JJABC') == ht_3ofaKind
assert get_hand_type('JJAAB') == ht_4ofaKind
assert get_hand_type('JJAAA') == ht_5ofaKind
assert get_hand_type('JABCD') == ht_OnePair
assert get_hand_type('JAABC') == ht_3ofaKind
assert get_hand_type('JAAAB') == ht_4ofaKind
assert get_hand_type('JAAAA') == ht_5ofaKind
assert get_hand_type('JAABB') == ht_FullHouse

assert get_sortable_hand('54321') == ht_HighCard + '54321'
assert get_sortable_hand('AKQJT') == ht_OnePair + 'EDC0A'

print("ALL TESTS PASSED")

YEAR = 2023
DAY = 7

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 5905
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 253866470
print("ANSWER CORRECT")
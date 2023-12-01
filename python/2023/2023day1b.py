from utilities import *
import math
import copy


digit_words = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}

def find_all_positions(line):
    positions = {}

    # look for numbers
    for i in range(1, 10):
        pos = line.find(str(i))
        while pos > -1:
            positions[pos] = i
            pos = line.find(str(i), pos+1)

    # look for words
    for word, number in digit_words.items():
        pos = line.find(word)
        while pos > -1:
            positions[pos] = number
            pos = line.find(word, pos+1)
    
    #print(positions)
    return positions

def find_first_digit(positions):
    (_, smallest_position) = sorted(positions.items())[0]
    return smallest_position

def find_last_digit(positions):
    (_, largest_position) = sorted(positions.items(), reverse=True)[0]
    return largest_position

def execute(input):
    print(input)

    sum = 0    

    for line in input:
        positions = find_all_positions(line)
        first_digit = find_first_digit(positions)
        last_digit = find_last_digit(positions)
        value = first_digit * 10 + last_digit
        #print(f"{line} ==> {value}")
        sum += value

    result = sum
    print(f"result: {result}")
    return result

# TESTS
assert find_all_positions("fivefiveggrbf8vcdftdpzhc68fiveggr") == {24: 6, 13: 8, 25: 8, 0: 5, 4: 5, 26: 5}
assert find_first_digit(find_all_positions("4nineeightseven2")) == 4
assert find_first_digit(find_all_positions("eightwothree")) == 8
assert find_first_digit(find_all_positions("fivefiveggrbf8vcdftdpzhc68fiveggr")) == 5
assert find_last_digit(find_all_positions("4nineeightseven2")) == 2
assert find_last_digit(find_all_positions("eightwothree")) == 3
assert find_last_digit(find_all_positions("fivefiveggrbf8vcdftdpzhc68fiveggr")) == 5
print("ALL TESTS PASSED")

YEAR = 2023
DAY = 1

#TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 281
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 54845
print("ANSWER CORRECT")
from utilities import *
import math
import copy


digit_words = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}

def execute(input):
    print(input)

    input_replaced = []
    for line in input:
        line_replaced = line
        for word, number in digit_words.items():
            line_replaced = line_replaced.replace(word, str(number))
        print(f"{line} ==> {line_replaced}")
        input_replaced.append(line_replaced)

    sum = 0    

    for line in input_replaced:
        digits = ""
        for char in line:
            if char.isdigit():
                digits += char
        print(f"{line} ==> {digits[0] + digits[-1]}")
        sum += int(digits[0] + digits[-1])

    result = sum
    print(f"result: {result}")
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

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
assert execute(input) == 0
print("ANSWER CORRECT")
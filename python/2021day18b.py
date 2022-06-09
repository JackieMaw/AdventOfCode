#TODO - how to share utilities across folders? do I need to make a package?
from abc import ABC, abstractmethod
from os import execl
from utilities import *
import math
import copy

class SnailFishNumber(ABC):

    def __init__(self, parent):
        self.parent = parent

    @abstractmethod
    def get_magnitude(self):
        ...

class LiteralSnailFishNumber(SnailFishNumber):

    def __init__(self, literal, parent = None):
        self.parent = parent
        self.literal = literal

    # The magnitude of a regular number is just that number.
    def get_magnitude(self):
        return self.literal

class PairSnailFishNumber(SnailFishNumber):

    def __init__(self, left, right, parent = None):
        self.parent = parent
        self.left = left
        self.right = right

    # The magnitude of a pair is 3 times the magnitude of its left element 
    # plus 2 times the magnitude of its right element. 
    def get_magnitude(self):
        return self.left.get_magnitude() * 3 + self.right.get_magnitude() * 2

def parse_snailfish_literal(number):
    return LiteralSnailFishNumber(int(number))

def parse_snailfish_number(number):
    # [1,2]
    # [[[[1,2]]],[[[3,4]]]]

    if number[0] != "[":
        return parse_snailfish_literal(number)

    # split the string into left and right, ignoring the first and last char
    nesting = 0
    for ptr in range(1, len(number) - 1):
        if number[ptr] == "[":
            nesting += 1
        elif number[ptr] == "]":
            nesting -= 1
        elif number[ptr] == "," and nesting == 0:
            # SPLIT HERE
            break

    s1 = number[1:ptr]
    s2 = number[ptr+1:-1]

    left = parse_snailfish_number(s1)
    right = parse_snailfish_number(s2)

    return PairSnailFishNumber(left, right)

def add(number1, number2):
    new_number = f"[{number1},{number2}]"
    #print(f"add {number1} + {number2} = {new_number}")
    return new_number

def explode_at(number, ptr):

    # extract the left number for the exploding pair

    left_ptr_start = ptr + 1
    left_ptr_end = left_ptr_start + 1
    while left_ptr_end < len(number) and number[left_ptr_end] not in ["[", "]", ","]:
        left_ptr_end += 1
    left_number = int(number[left_ptr_start:left_ptr_end])

    # extract the right number for the exploding pair

    right_ptr_start = left_ptr_end + 1
    right_ptr_end = right_ptr_start + 1
    while right_ptr_end < len(number) and number[right_ptr_end] not in ["[", "]", ","]:
        right_ptr_end += 1
    right_number = int(number[right_ptr_start:right_ptr_end])

    #print(f"explode [{left_number},{right_number}] @ {ptr}")

    s1 = number[:ptr] # the beginning of the string will remain the same
    s2 = number[right_ptr_end+1:] # the end of the string will remain the same

    assert f"{s1}[{left_number},{right_number}]{s2}" == number

    # look for the neighbour to the left

    new_left_ptr_end = len(s1) - 1
    while new_left_ptr_end > 0 and s1[new_left_ptr_end] in ["[", "]", ","]: # keep looking for a number on the left
        new_left_ptr_end -= 1

    if new_left_ptr_end > 0: # we found a number on the left, now where does this number start?
        new_left_ptr_start = new_left_ptr_end
        while new_left_ptr_start > 0 and s1[new_left_ptr_start] not in ["[", "]", ","]:
            new_left_ptr_start -= 1
        new_left_ptr_start += 1 # we found the first non-numeric, so the number must start after that
        old_left_number = int(s1[new_left_ptr_start:new_left_ptr_end + 1])
        new_left_number = left_number + old_left_number 
        #print(f"*** LHS {left_number} ==> {old_left_number} + {left_number} = {new_left_number}")
        s1 = s1[:new_left_ptr_start] + str(new_left_number) + s1[new_left_ptr_end + 1:]

    # look for the neighbour to the right

    new_right_ptr = 0
    while new_right_ptr < len(s2) and s2[new_right_ptr] in ["[", "]", ","]:
        new_right_ptr += 1

    if new_right_ptr < len(s2):
        new_right_ptr_end = new_right_ptr + 1
        while new_right_ptr_end < len(s2) and s2[new_right_ptr_end] not in ["[", "]", ","]:
            new_right_ptr_end += 1
        old_right_number = int(s2[new_right_ptr:new_right_ptr_end])
        new_right_number = right_number + old_right_number        
        #print(f"*** RHS {right_number} ==> {old_right_number} + {right_number} = {new_right_number}")
        s2 = s2[:new_right_ptr] + str(new_right_number) + s2[new_right_ptr_end:]
       
    return s1 + "0" + s2

def explode(number):

    # walk through the number from left to right, counting the nesting level by counting the brackets
    # as soon as you get to a nesting level of 5 we know we are too deep and we need to "expode" this number (prune the branch)

    nesting = 0
    for ptr in range(len(number)):
        if number[ptr] == "[":
            nesting += 1
        elif number[ptr] == "]":
            nesting -= 1
        if nesting == 5:
            exploded_number = explode_at(number, ptr)
            #print(f"explode {number} => {exploded_number}")
            return exploded_number, True

    return number, False

def split_at(number, ptr):

    end_ptr = ptr + 1
    while end_ptr < len(number) and number[end_ptr] not in ["[", "]", ","]:
        end_ptr += 1

    s1 = number[:ptr]
    s2 = number[end_ptr:]

    number_to_split = int(number[ptr:end_ptr])
    new_split_number = f"[{math.floor(number_to_split/2)},{math.ceil(number_to_split/2)}]"
       
    return s1 + new_split_number + s2


def split(number):

    # walk through the number from left to right, checking to see if there is any two-digit number, ie: 10 or greater
    # as soon as you find one we know the number is too big and we need to "split" this number into a pair (make a new branch)

    for ptr in range(len(number) - 1):
        if number[ptr] not in ["[", "]", ","] and number[ptr + 1] not in ["[", "]", ","]:
            split_number = split_at(number, ptr)
            #print(f"split {number} => {split_number}")
            return split_number, True

    return number, False

def reduce(number):

    reduced = True
    while reduced:
        number, reduced = explode(number)
        if not reduced:
            number, reduced = split(number) 
    
    return number

def add_numbers(number1, number2):
    result = add(number1, number2)
    result_reduced = reduce(result)
    # print(f"  {number1}")
    # print(f"+ {number2}")
    # print(f"= {result_reduced}")
    # print()
    return result_reduced

def add_list(numbers):

    result = None
    for number in numbers:
        if result is None:
            result = number
        else:
            result = add_numbers(result, number)
    return result

def get_magnitude(number):

    snail_fish_number = parse_snailfish_number(number)

    return snail_fish_number.get_magnitude()

def execute(input):
    #print(input)

    max_magnitude = 0
    i = 0
    max_i = len(input) * (len(input) - 1)

    for number1 in input:
        for number2 in input:
            if number1 != number2:             
                i += 1
                print(f"Computing {i} of {max_i}...")   
                result = add_numbers(number1, number2)
                magnitude = get_magnitude(result)
                if magnitude > max_magnitude:
                    max_magnitude = magnitude

    print(f"max_magnitude: {max_magnitude}") 
    return max_magnitude

# TESTS

numberA = PairSnailFishNumber(LiteralSnailFishNumber(9), LiteralSnailFishNumber(1))
assert numberA.get_magnitude() == 29
numberB = PairSnailFishNumber(LiteralSnailFishNumber(1), LiteralSnailFishNumber(9))
assert numberB.get_magnitude() == 21
assert PairSnailFishNumber(numberA, numberB).get_magnitude() == 129

assert add("[1,2]","[[3,4],5]") == "[[1,2],[[3,4],5]]"
assert explode("[[[[[9,8],1],2],3],4]") == ("[[[[0,9],2],3],4]", True)
assert explode("[7,[6,[5,[4,[3,2]]]]]") == ("[7,[6,[5,[7,0]]]]", True)
assert explode("[[6,[5,[4,[3,2]]]],1]") == ("[[6,[5,[7,0]]],3]", True)
assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", True)
assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == ("[[3,[2,[8,0]]],[9,[5,[7,0]]]]", True)
assert split("[11,5]") == ("[[5,6],5]", True)
assert add("[[[[4,3],4],4],[7,[[8,4],9]]]","[1,1]") == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
assert reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

assert explode("[[[[[109,108],21],2],3],4]") == ("[[[[0,129],2],3],4]", True)

print("ALL TESTS PASSED")

YEAR = 2021
DAY = 18

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test1")
input = get_strings(raw_input)
assert add_list(input) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
print("TEST INPUT 1 PASSED")

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert add_list(input) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
print("TEST INPUT 2 PASSED")

raw_input = get_input(YEAR, DAY, "_test3")
input = get_strings(raw_input)
assert add_list(input) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"
print("TEST INPUT 3 PASSED")

assert get_magnitude("[9,1]") == 29
assert get_magnitude("[1,9]") == 21
assert get_magnitude("[[9,1],[1,9]]") == 129

test4_line7 = ["[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]", "[2,9]"]
assert add_list(test4_line7) == "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]"

raw_input = get_input(YEAR, DAY, "_test4")
input = get_strings(raw_input)
result = add_list(input)
assert result == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
print("TEST INPUT 4 PASSED")

raw_input = get_input(YEAR, DAY, "_test5")
input = get_strings(raw_input)
result = add_list(input)
assert result == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
assert get_magnitude(result) == 4140
print("TEST INPUT 5 PASSED - CORRECT MAGNITUDE")

assert execute(input) == 3993
print("TEST INPUT 5 PASSED - LARGEST MAGNITUDE")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 4664
print("ANSWER CORRECT")
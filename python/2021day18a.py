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

def add_simple(number1, number2):
    new_number = f"[{number1},{number2}]"
    print(f"add_simple {number1} + {number2} = {new_number}")
    return new_number

def explode_at(number, ptr):
    # number[ptr] = "["
    left_number = int(number[ptr+1])
    right_number = int(number[ptr+3])

    s1 = number[:ptr]
    s2 = number[ptr+5:]

    new_left_ptr = len(s1) - 1
    while new_left_ptr > 0 and s1[new_left_ptr] in ["[", "]", ","]:
        new_left_ptr -= 1

    if new_left_ptr > 0:
        new_left_number = left_number + int(s1[new_left_ptr])
        s1 = s1[:new_left_ptr] + str(new_left_number) + s1[new_left_ptr+1:]

    new_right_ptr = 0
    while new_right_ptr < len(s2) and s2[new_right_ptr] in ["[", "]", ","]:
        new_right_ptr += 1

    if new_right_ptr < len(s2):
        new_right_number = right_number + int(s2[new_right_ptr])
        s2 = s2[:new_right_ptr] + str(new_right_number) + s2[new_right_ptr+1:]
       
    return s1 + "0" + s2

def explode(number):

    nesting = 0
    for ptr in range(len(number)):
        if number[ptr] == "[":
            nesting += 1
        elif number[ptr] == "]":
            nesting -= 1
        if nesting == 5:
            exploded_number = explode_at(number, ptr)
            print(f"explode {number} => {exploded_number}")
            return exploded_number, True

    return number, False

def split_at(number, ptr):

    # number[ptr] = "201"

    end_ptr = ptr + 1
    while end_ptr < len(number) and number[end_ptr] not in ["[", "]", ","]:
        end_ptr += 1

    s1 = number[:ptr]
    s2 = number[end_ptr:]

    number_to_split = int(number[ptr:end_ptr])
    new_split_number = f"[{math.floor(number_to_split/2)},{math.ceil(number_to_split/2)}]"
       
    return s1 + new_split_number + s2


def split(number):

    for ptr in range(len(number) - 1):
        if number[ptr] not in ["[", "]", ","] and number[ptr + 1] not in ["[", "]", ","]:
            split_number = split_at(number, ptr)
            print(f"split {number} => {split_number}")
            return split_number, True

    return number, False

def reduce(number):

    reduced = True
    while reduced:
        number, reduced = explode(number)
        if not reduced:
            number, reduced = split(number) 
    
    return number

def add_list(numbers):

    result = None
    for number in numbers:
        if result is None:
            result = number
        else:
            result = add_simple(result, number)
            result = reduce(result)
    return result

def get_magnitude(number):
    return 0

def execute(input):
    print(input)

    number = add_list(input)

    result = get_magnitude(number)
    print(f"result: {result}") 
    return result

# TESTS

numberA = PairSnailFishNumber(LiteralSnailFishNumber(9), LiteralSnailFishNumber(1))
assert numberA.get_magnitude() == 29
numberB = PairSnailFishNumber(LiteralSnailFishNumber(1), LiteralSnailFishNumber(9))
assert numberB.get_magnitude() == 21
assert PairSnailFishNumber(numberA, numberB).get_magnitude() == 129

assert add_simple("[1,2]","[[3,4],5]") == "[[1,2],[[3,4],5]]"
assert explode("[[[[[9,8],1],2],3],4]") == ("[[[[0,9],2],3],4]", True)
assert explode("[7,[6,[5,[4,[3,2]]]]]") == ("[7,[6,[5,[7,0]]]]", True)
assert explode("[[6,[5,[4,[3,2]]]],1]") == ("[[6,[5,[7,0]]],3]", True)
assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", True)
assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == ("[[3,[2,[8,0]]],[9,[5,[7,0]]]]", True)
assert split("[11,5]") == ("[[5,6],5]", True)
assert add_simple("[[[[4,3],4],4],[7,[[8,4],9]]]","[1,1]") == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
assert reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

assert get_magnitude("[9,1]") == 29
assert get_magnitude("[1,9]") == 21
assert get_magnitude("[[9,1],[1,9]]") == 129

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

raw_input = get_input(YEAR, DAY, "_test4")
input = get_strings(raw_input)
assert add_list(input) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
print("TEST INPUT 4 PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
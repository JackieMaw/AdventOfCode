#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def execute(input):
    print(input)

    number = add_list(input)

    result = get_magniture(number)
    print(f"result: {result}") 
    return result

# TESTS
assert add("[1,2]","[[3,4],5]") == "[[1,2],[[3,4],5]]"
assert reduce("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
assert reduce("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
assert reduce("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
assert reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
assert add("[[[[4,3],4],4],[7,[[8,4],9]]]","[1,1]") == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]"
assert reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
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

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert add_list(input) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
print("TEST INPUT 2 PASSED")

raw_input = get_input(YEAR, DAY, "_test2")
input = get_strings(raw_input)
assert add_list(input) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
print("TEST INPUT 2 PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
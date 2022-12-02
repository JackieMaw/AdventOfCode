#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy


pairs = { "[" : "]", "(" : ")", "{" : "}", "<" : ">" }

# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.
points = { ")" : 3, "]" : 57, "}" : 1197, ">" : 25137 }

score = None

def process_chunk(chunk):
    
    global score
    print(f"Processing Chunk: {chunk}")          

    c_start = chunk[0]
    
    if c_start in pairs:
        if len(chunk) == 1:
            print(f"Chunk is INCOMPLETE: {chunk}")
            return "INCOMPLETE"     
        c_end_expected = pairs[c_start]
        rest = chunk[1:]
        c_next = rest[0]
        while c_next in pairs:  # the next char is OPEN, so we found the start of a new chunk
            rest = process_chunk(rest)
            if rest == "INCOMPLETE" or rest == "CORRUPTED":
                return rest
            if len(rest) == 0:
                print(f"Chunk is INCOMPLETE: {chunk}")
                return "INCOMPLETE"  
            c_next = rest[0]
        # now we definately expect an end!
        if c_next == c_end_expected:
            return rest[1:]
        else:
            print(f"Chunk is CORRUPTED: {chunk}")
            if score is None:
                score = points[c_next]
                print(f"First Invalid Character: {c_next} earns score: {score}")
            return "CORRUPTED"           
        
    else:
        # chunk must start with OPEN
        print(f"Chunk is CORRUPTED: {chunk}")
        if score is None:
            score = points[c_start]
            print(f"First Invalid Character: {c_start} earns score: {score}")
        return "CORRUPTED"      

def is_valid_chunk(chunk):
    global score
    score = None
    print(f"Testing Chunk: {chunk}")
    leftover = process_chunk(chunk)
    return leftover == ""

def get_score(chunk):
    global score
    score = None
    print(f"Testing Chunk: {chunk}")
    leftover = process_chunk(chunk)
    if leftover != "" and score is not None:
        return score
    return 0

def execute(input):
    print(input)

    total_score = 0
    for chunk in input:
        total_score += get_score(chunk)
   
    result = total_score
    print(f"result: {result}") 
    return result

# TESTS

assert is_valid_chunk("()") == True
assert is_valid_chunk(")") == False
assert is_valid_chunk("(") == False
assert is_valid_chunk("(]") == False
assert is_valid_chunk("([])") == True
assert is_valid_chunk("<([{}])>") == True
assert is_valid_chunk("[<>({}){}[([])<>]]") == True
assert is_valid_chunk("(((((((((())))))))))") == True
assert get_score("()") == 0
assert get_score("(") == 0
assert get_score(")") == 3
assert get_score("[({(<(())[]>[[{[]{<()<>>") == 0
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 10

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 26397
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 399153
print("ANSWER CORRECT")
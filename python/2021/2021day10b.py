#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy


pairs = { "[" : "]", "(" : ")", "{" : "}", "<" : ">" }

# ): 1 point.
# ]: 2 points.
# }: 3 points.
# >: 4 points.
points = { ")" : 1, "]" : 2, "}" : 3, ">" : 4 }

score = 0

def complete(open):                   
    close = pairs[open] 
    global score
    score = score * 5 + points[close]
    #print(f"Completion Required: {close} earns score: {score}")

def process_chunk(chunk):
    
    #print(f"Processing Chunk: {chunk}")          

    c_start = chunk[0]
    
    if c_start in pairs:
     

        if len(chunk) == 1:            
            #print(f"Chunk is INCOMPLETE: {chunk}")
            complete(c_start)
            return "INCOMPLETE"

        rest = chunk[1:]
        c_next = rest[0]

        while c_next in pairs:  # the next char is OPEN, so we found the start of a new chunk
            rest = process_chunk(rest)
            if rest == "INCOMPLETE":
                complete(c_start)
                return rest
            if rest == "CORRUPTED":
                return rest
            if len(rest) == 0:
                #print(f"Chunk is INCOMPLETE: {chunk}")
                complete(c_start)
                return "INCOMPLETE"  
            c_next = rest[0]

        # now we definately expect a CLOSE!
        c_end_expected = pairs[c_start]
        if c_next == c_end_expected:
            return rest[1:]
        else:
            #print(f"Chunk is CORRUPTED: {chunk}")
            return "CORRUPTED"           
        
    else:
        # chunk must start with OPEN
        #print(f"Chunk is CORRUPTED: {chunk}")
        return "CORRUPTED"      

def calculate_score(chunk):
    global score
    score = 0
    #print(f"get_score: {chunk}")
    do = True
    while do:
        chunk = process_chunk(chunk)
        #print(f"leftover: {chunk} score: {score}")
        if chunk in ["CORRUPTED", "INCOMPLETE"] or len(chunk) == 0:
            do = False
    return score

def execute(input):
    print(input)

    all_scores = []
    for chunk in input:
        this_score = calculate_score(chunk)
        print(f"score: {this_score} for chunk:{chunk}")
        if this_score > 0:
            all_scores.append(this_score)
   
    all_scores.sort()

    result = all_scores[math.floor(len(all_scores) / 2)]
    print(f"result: {result}") 
    return result

# TESTS
assert calculate_score("(") == 1
assert calculate_score("[") == 2
assert calculate_score("{") == 3
assert calculate_score("<") == 4
assert calculate_score("[({(<(())[]>[[{[]{<()<>>") == 288957

assert calculate_score("({[<{<<[]>>(") == 5566
assert calculate_score("[(()[<>])]") == 0
assert calculate_score("[(()[<>])]({[<{<<[]>>(") == 5566

assert calculate_score("(((({<>}<{<{<>}{[]{[]{}") == 1480781
assert calculate_score("{<[[]]>}<{[{[{[]{()[[[]") == 995444
assert calculate_score("<{([{{}}[<[[[<>{}]]]>[]]") == 294
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 10

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 288957
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 2995077699
print("ANSWER CORRECT")
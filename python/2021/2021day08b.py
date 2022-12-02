#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

def get_digitizer():
    digitzer = { "abcefg" : 0, "cf" : 1, "acdeg" : 2, "acdfg" : 3, "bcdf" : 4, "abdfg" : 5, "adbefg" : 6, "acf" : 7, "abcdefg" : 8, "abcdfg" : 9}
    return digitzer

def translate_digitizer(original_digitizer, map):
    new_digitizer = { translate(key, map):value for (key,value) in original_digitizer.items() }
    return new_digitizer

def translate(string, translator):    
    return "".join(sorted([ translator[char] for char in string ]))

def get_clues(digitzer, signals):
    clues = {}
    for key in digitzer.keys():
        clues[key] = []
    
    for signal in signals:
        signal_length = len(signal)
        for key in digitzer.keys():
            if len(key) == signal_length:
                clues[key].append(signal)
    #print(clues)
    return clues

def get_translator(clues):    
    translator = { } 

    counter = 1
    already_used_to_refine = []
    while len(translator) < 7:
        #
        # walk through all your clues and see if we can reduce the other clues
        for source in sorted(clues.keys(), key=len, reverse=True):
            targets = clues[source]
            if len(targets) == 1: # we can use this clue to refine/reduce other clues
                target = targets[0]
                if source not in already_used_to_refine:
                    already_used_to_refine.append(source)

                    #print(f"Attempting to refine with: {source}")
                    clues_to_remove = []
                    clues_to_add = {}
                    for source_to_refine, targets_to_refine in clues.items():
                        refined = refine(source, target, source_to_refine, targets_to_refine)
                        if refined is not None:
                            (new_source, new_targets) = refined
                            clues_to_remove.append(source_to_refine)
                            #print(f"Successfully refined {source_to_refine} to {new_source}")
                            clues_to_add[new_source] = new_targets
                            if len(new_source) == 1:
                                # we have a winner!
                                #print(f"TRANSLATION FOUND: {new_source} to {new_targets[0]}")
                                translator[new_source] = new_targets[0]
                    
                    #print(f"Added {len(clues_to_add)} new clues and removed {len(clues_to_remove)} old clues.")
                    for clue_to_remove in clues_to_remove:
                        clues.pop(clue_to_remove)
                    clues.update(clues_to_add)

        counter += 1
        #print(f"Pass completed: {counter}. Translator now has {len(translator)} values.")

    return translator

def refine(source, target, source_to_refine, targets_to_refine):
    # if source_to_refine contains all the characters from source
    # return a new clue for source_to_refine - source
    if len(source_to_refine) > len(source):
        new_source = remove_from(source_to_refine, source)
        if new_source is not None:
            new_targets = { remove_from(target_to_refine, target) for target_to_refine in targets_to_refine } 
            valid_targets = [ target for target in new_targets if target is not None ]
            return (new_source, valid_targets)
    return None

def remove_from(string, string_to_remove):
    new_string = string.translate({ord(i): None for i in string_to_remove})
    if len(string) - len(new_string) == len(string_to_remove):
        return new_string
    return None

def decode(line):
    sparts = line.split("|")
    signals = sparts[0].split()
    output_values = sparts[1].split()

    digitizer = get_digitizer()
    clues = get_clues(digitizer, signals)
    translator = get_translator(clues)

    new_digitizer = translate_digitizer(digitizer, translator)
    output = ""
    for output_value in output_values:
        output_value_sorted = "".join(sorted(output_value))
        digit = new_digitizer[output_value_sorted]
        output += str(digit)

    #print(f"output: {output}")

    return int(output)

def execute(input):
    sum = 0
    for line in input:
        sum += decode(line)

    result = sum
    print(f"result: {result}") 
    return result

# TESTS
assert decode("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf") == 5353
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 8

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 61229
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 998900
print("ANSWER CORRECT")
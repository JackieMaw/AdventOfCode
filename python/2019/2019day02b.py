#TODO - how to share utilities?
from utilities.utilities import *
import math
import copy

def execute(input_data):
    for noun in range(1, 100):
        for verb in range(1, 100):
            temp_input_data = copy.deepcopy(input_data)  
            temp_input_data[1] = noun
            temp_input_data[2] = verb
            answer =  run_intcode(temp_input_data)
            #print(f"{noun} {verb} => {answer}")
            if (answer == 19690720):
                return 100 * noun + verb;

def run_intcode(input_data):
    program_counter = 0    
    while program_counter + 3 < len(input_data):
        opcode = input_data[program_counter]
        if opcode == 99:
            break
        input1ptr = input_data[program_counter + 1]
        input1 = input_data[input1ptr]
        input2ptr = input_data[program_counter + 2]
        input2 = input_data[input2ptr]
        output = 0
        if opcode == 1:
            output = input1 + input2
        elif opcode == 2:
            output = input1 * input2            
        output_ptr = input_data[program_counter + 3]
        input_data[output_ptr] = output
        program_counter += 4
    return input_data[0]

assert run_intcode([1,0,0,0,99]) == 2
assert run_intcode([2,3,0,3,99]) == 2
assert run_intcode([2,4,4,5,99,0]) == 2
assert run_intcode([1,1,1,4,99,5,6,0,99]) == 30
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 2
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers_csv(raw_input)
assert execute(input) == 9342
print("ANSWER CORRECT")
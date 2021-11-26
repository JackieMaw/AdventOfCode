#TODO - how to share utilities?
from utilities import *
import math

def execute(input_data):
    #replace position 1 with the value 12 and replace position 2 with the value 2
    input_data[1] = 12
    input_data[2] = 2
    return run_intcode(input_data)

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
#download_input(YEAR, DAY)
input_data = get_integers_csv(YEAR, DAY)
print(execute(input_data))
#2894520
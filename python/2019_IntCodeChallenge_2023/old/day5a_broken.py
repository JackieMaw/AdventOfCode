o0lk,i.'/[def init_memory(intcode_program):
    memory = {}
    for memory_pointer in range(len(intcode_program)):
        memory[memory_pointer] = intcode_program[memory_pointer]
    return memory

def add(memory, instruction_pointer):
    input1ptr = memory[instruction_pointer + 1]
    if mode1 == 1:
        input1 = input1ptr
    else:
        input1 = memory[input1ptr]
  
    input2ptr = memory[instruction_pointer + 2]
    if mode2 == 1:
        input2 = input2ptr
    else:
        input2 = memory[input2ptr]
  
    print(f"Add: {input1} + {input2}")
    output = input1 + input2
    output_ptr = memory[instruction_pointer + 3]
    memory[output_ptr] = output
  
    instruction_pointer += 4

"""
"""
def run_intcode(intcode_program, input_handler, output_handler):
    memory = init_memory(intcode_program)

    instruction_pointer = 0
    while True:

        print(f"Instruction Pointer: {instruction_pointer}")
        full_opcode = memory[instruction_pointer]
        print(f"OpCode: {full_opcode}")
        params = [
            memory.get(instruction_pointer + 1, None),
            memory.get(instruction_pointer + 2, None),
            memory.get(instruction_pointer + 3, None)
        ]
        print(f"Params: {params}")
        full_opcode_str = str(full_opcode)

        opcode = full_opcode % 100

        while len(full_opcode_str) < 5:
            full_opcode_str = "0" + full_opcode_str

        mode1 = int(full_opcode_str[0:1])
        mode2 = int(full_opcode_str[1:2])
        mode3 = int(full_opcode_str[2:3])
        print(f"Modes: {full_opcode_str} => {mode1} {mode2} {mode3}")

        if opcode == 99:
            return_code = memory[0]
            print(f"Program Terminated. Return code: {return_code}")
            return return_code

        if opcode == OPERATION.ADD:  #ADD
            instruction_pointer = add(memory, instruction_pointer)

        elif opcode == OPERATION.MULTIPLY:  #MULTIPLY
            input1ptr = memory[instruction_pointer + 1]
            if mode1 == 1:
                input1 = input1ptr
            else:
                input1 = memory[input1ptr]

            input2ptr = memory[instruction_pointer + 2]
            if mode2 == 1:
                input2 = input2ptr
            else:
                input2 = memory[input2ptr]

            print(f"Multiply: {input1} x {input2}")
            output = input1 * input2
            output_ptr = memory[instruction_pointer + 3]
            memory[output_ptr] = output
            instruction_pointer += 4

        elif opcode == OPERATION_INPUT:  
            input_to_save = input_handler.pop(0)
            #input_to_save = input("INPUT: ")
            print(f"INPUT: {input_to_save}")
            #print(f"Input Handler Remaining: {input_handler}")
            output_ptr = memory[instruction_pointer + 1]
            memory[output_ptr] = input_to_save
            instruction_pointer += 2

        elif opcode == 4:  #OUTPUT
            output_ptr = memory[instruction_pointer + 1]
            output = memory[output_ptr]
            print(f"OUTPUT: {output}")
            output_handler.append(output)
            #print(f"Output Handler Remaining: {output_handler}")
            instruction_pointer += 2

        else:
            raise Exception(f"Unsupported OpCode: {opcode}")

    return None


def execute(intcode_program, input_handler, output_handler):
    run_intcode(intcode_program, input_handler, output_handler)
    diagnostic_code = output_handler[0]
    print(f"Diagnostic Test Completed. Diagnostic code: {diagnostic_code}")
    return diagnostic_code


def execute_all():

    test_data = [int(l) for l in "3,0,4,0,99".split(",")]
    expected_result = 5
    input_handler = [expected_result]
    output_handler = []
    test_result = execute(test_data, input_handler, output_handler)
    assert test_result == expected_result

    test_data = [int(l) for l in "1002,4,3,4,33".split(",")]
    test_result = run_intcode(test_data, [], [])
    assert test_result == 1002
    print(f"TESTS PASSED!")

    # ACTUAL
    with open("./input/day5_actual.txt", "r") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    input_handler = [1]
    output_handler = []
    result = execute(intcode_program, input_handler, output_handler)
    print(f"ACTUAL Result: {result}")
    assert result == 7157989
    print(f"ACTUAL PASSED!")

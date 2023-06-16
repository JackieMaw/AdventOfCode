def init_memory(input_data):
    memory_space = {}
    for i in range(len(input_data)):
        memory_space[i] = input_data[i]
    return memory_space


def run_intcode(input_data):
    program_counter = 0
    while True:

        opcode = input_data[program_counter]

        if opcode == 99:
            break

        input1ptr = input_data[program_counter + 1]
        input1 = input_data[input1ptr]

        input2ptr = input_data[program_counter + 2]
        input2 = input_data[input2ptr]

        output = 0
        if opcode == 1:  #ADD
            output = input1 + input2
        elif opcode == 2:  #MULTIPLY
            output = input1 * input2

        output_ptr = input_data[program_counter + 3]
        input_data[output_ptr] = output

        program_counter += 4

    return input_data[0]


def execute(input_data):

    for noun in range(0, 100):
        for verb in range(0, 100):
            memory_space = init_memory(input_data)
            memory_space[1] = noun
            memory_space[2] = verb
            return_code = run_intcode(memory_space)
            if return_code == 19690720:
                return 100 * noun + verb

    raise Exception("Couldn't get the answer")


def execute_all():

    assert run_intcode([1, 0, 0, 0, 99]) == 2
    assert run_intcode([2, 3, 0, 3, 99]) == 2
    assert run_intcode([2, 4, 4, 5, 99, 0]) == 2
    assert run_intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
    print("ALL TESTS PASSED")

    # ACTUAL
    with open("./input/day2_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    #BUG - memory_space should be initialized inside the loop
    #memory_space = init_memory(input_data)
    result = execute(input_data)
    print(f"ACTUAL Result: {result}")
    assert result == 8609
    print(f"ACTUAL PASSED!")

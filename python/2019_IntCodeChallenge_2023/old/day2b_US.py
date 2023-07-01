def init_memory(intcode_program):
    memory = {}
    for memory_pointer in range(len(intcode_program)):
        memory[memory_pointer] = intcode_program[memory_pointer]
    return memory


def run_intcode(memory_space):
    program_counter = 0
    while True:

        opcode = memory_space[program_counter]

        if opcode == 99:
            break

        input1ptr = memory_space[program_counter + 1]
        input1 = memory_space[input1ptr]

        input2ptr = memory_space[program_counter + 2]
        input2 = memory_space[input2ptr]

        output = 0
        if opcode == 1:  #ADD
            output = input1 + input2
        elif opcode == 2:  #MULTIPLY
            output = input1 * input2

        output_ptr = memory_space[program_counter + 3]
        memory_space[output_ptr] = output

        program_counter += 4

    return memory_space[0]


def execute(intcode_program):

    #BUG
    #memory_space = init_memory(intcode_program)

    for noun in range(0, 100):
        for verb in range(0, 100):

            memory_space = init_memory(intcode_program)
            memory_space[1] = noun
            memory_space[2] = verb
            return_code = run_intcode(memory_space)

            if return_code == 19690720:
                return 100 * noun + verb


def execute_all():

    assert run_intcode([1, 0, 0, 0, 99]) == 2
    assert run_intcode([2, 3, 0, 3, 99]) == 2
    assert run_intcode([2, 4, 4, 5, 99, 0]) == 2
    assert run_intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
    print("ALL TESTS PASSED")

    # ACTUAL
    with open("./input/day2_actual.txt", "r") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    #BUG - memory_space should be initialized inside the loop
    #memory_space = init_memory(intcode_program)

    result = execute(intcode_program)
    print(f"ACTUAL Result: {result}")
    assert result == 8609
    print(f"ACTUAL PASSED!")

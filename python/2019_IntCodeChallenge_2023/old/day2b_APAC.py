def init_memory(intcode_program):
    memory_space = {}
    for i in range(len(intcode_program)):
        memory_space[i] = intcode_program[i]
    return memory_space


def run_intcode(intcode_program):
    program_counter = 0
    while True:

        opcode = intcode_program[program_counter]

        if opcode == 99:
            break

        input1ptr = intcode_program[program_counter + 1]
        input1 = intcode_program[input1ptr]

        input2ptr = intcode_program[program_counter + 2]
        input2 = intcode_program[input2ptr]

        output = 0
        if opcode == 1:  #ADD
            output = input1 + input2
        elif opcode == 2:  #MULTIPLY
            output = input1 * input2

        output_ptr = intcode_program[program_counter + 3]
        intcode_program[output_ptr] = output

        program_counter += 4

    return intcode_program[0]


def execute(intcode_program):

    for noun in range(0, 100):
        for verb in range(0, 100):
            memory_space = init_memory(intcode_program)
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
    with open("./input/day2_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    #BUG - memory_space should be initialized inside the loop
    #memory_space = init_memory(intcode_program)
    result = execute(intcode_program)
    print(f"ACTUAL Result: {result}")
    assert result == 8609
    print(f"ACTUAL PASSED!")

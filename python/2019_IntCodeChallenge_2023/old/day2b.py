def init_memory(intcode_program):
    memory = {}
    for memory_pointer in range(len(intcode_program)):
        memory[memory_pointer] = intcode_program[memory_pointer]
    return memory


def run_intcode(memory_space):

    instruction_pointer = 0
    while True:
        opcode = memory_space[instruction_pointer]
        if opcode == 99:
            break
        input1ptr = memory_space[instruction_pointer + 1]
        input1 = memory_space[input1ptr]
        input2ptr = memory_space[instruction_pointer + 2]
        input2 = memory_space[input2ptr]
        output = 0
        if opcode == 1:
            output = input1 + input2
        elif opcode == 2:
            output = input1 * input2
        output_ptr = memory_space[instruction_pointer + 3]
        memory_space[output_ptr] = output
        instruction_pointer += 4
    return memory_space[0]


def run_intcode_with(intcode_program, noun, verb):
    memory_space = init_memory(intcode_program)
    memory_space[1] = noun
    memory_space[2] = verb
    return run_intcode(memory_space)


def seek_output(intcode_program, seek):
    for noun in range(100):
        for verb in range(100):
            if run_intcode_with(intcode_program, noun, verb) == seek:
                return (noun, verb)
    return


def execute(intcode_program):
    (noun, verb) = seek_output(intcode_program, 19690720)
    return 100 * noun + verb


def execute_all():

    with open("./input/day2_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    assert run_intcode_with(intcode_program, 12, 2) == 3706713
    print("ALL TESTS PASSED")

    result = execute(intcode_program)
    print(f"ACTUAL Result: {result}")
    assert result == 8609
    print(f"ACTUAL PASSED!")

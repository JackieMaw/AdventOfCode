def run_intcode(intcode_program):
    program_counter = 0
    while program_counter + 3 < len(intcode_program):

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
    #replace position 1 with the value 12 and replace position 2 with the value 2
    intcode_program[1] = 12
    intcode_program[2] = 2
    return run_intcode(intcode_program)


def execute_all():

    assert run_intcode([1, 0, 0, 0, 99]) == 2
    assert run_intcode([2, 3, 0, 3, 99]) == 2
    assert run_intcode([2, 4, 4, 5, 99, 0]) == 2
    assert run_intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == 30
    print("ALL TESTS PASSED")

    # ACTUAL
    with open("./input/day2_actual.txt", "r", encoding="utf-8") as text_file:
        intcode_program = [int(l) for l in text_file.read().split(",")]

    result = execute(intcode_program)
    print(f"ACTUAL Result: {result}")
    assert result == 3706713
    print(f"ACTUAL PASSED!")

import model.IntCodeComputer

def test_execute_9a():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()
    result = computer.get_diagnostic_code()

    assert result == 2377080455

def test_execute_9b():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [2]
    output_stream = []
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()
    result = computer.get_diagnostic_code()

    assert result == 74917

def is_scaffold_or_robot(char):
    return char in ("#", "^", ">", "<", "v")

def is_intersection_point(view, row_counter, col_counter):
    point = view[row_counter][col_counter]
    if is_scaffold_or_robot(point):
        above = view[row_counter-1][col_counter]
        below = view[row_counter+1][col_counter]
        left = view[row_counter][col_counter-1]
        right = view[row_counter][col_counter+1]
        if is_scaffold_or_robot(above) and is_scaffold_or_robot(below) and is_scaffold_or_robot(left) and is_scaffold_or_robot(right):
            return True
    return False

def get_alignment_paramter(row_counter, col_counter):
    return row_counter * col_counter

def test_execute_17a():

    with open("./input/day17_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = []
    output_stream = []
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()

    ascii_output = to_ascii(output_stream)
    print(ascii_output)
    assert ascii_output[:15] == "..........####^"

    view = parse_view(ascii_output)

    num_rows = len(view)
    num_cols = len(view[0])

    sum_of_alignment_parameters = 0

    # intersections can never be on the edges so we skip the first and last rows and columns
    for row_counter in range(1, num_rows - 1):
        for col_counter in range(1, num_cols - 1):
            if is_intersection_point(view, row_counter, col_counter):
                sum_of_alignment_parameters += get_alignment_paramter(row_counter, col_counter)

    assert sum_of_alignment_parameters == 0


def to_ascii(output_stream):
    ascii_stream = ''.join(chr(i) for i in output_stream)
    return ascii_stream

def parse_view(ascii_output):
    return ascii_output.split("\n")
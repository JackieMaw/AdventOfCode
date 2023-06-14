import model.IntCodeComputer

def execute_diagnostic(input_data, input_stream, output_stream):
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run()
    diagnostic_code = output_stream[len(output_stream) - 1]
    return diagnostic_code


def test_execute_9a():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    result = execute_diagnostic(input_data, input_stream, output_stream)

    assert result == 2377080455

import model.IntCodeComputer

def execute(input_data, input_stream, output_stream):
    computer = model.IntCodeComputer.IntCodeComputer(input_data, input_stream, output_stream)
    computer.run_intcode()
    print(f"Diagnostic Test Completed.")
    print(f"All Outputs: {output_stream}")
    diagnostic_code = output_stream[len(output_stream) - 1]
    print(f"Diagnostic code: {diagnostic_code}")
    return diagnostic_code


def test_execute_all():

    with open("./input/day9_actual.txt", "r") as text_file:
        input_data = [int(l) for l in text_file.read().split(",")]

    input_stream = [1]
    output_stream = []
    result = execute(input_data, input_stream, output_stream)
    print(f" ==== ACTUAL Result: {result}  ====")

    assert result == 2369720
    print(f"ACTUAL PASSED!")

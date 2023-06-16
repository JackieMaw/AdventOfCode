def parse_input(input_lines):
  state = None
  return state

def execute(state):  
  result = None
  return result

def execute_all():

  # TEST
  with open("./input/day?_test.txt", "r") as text_file:
    input_lines = text_file.read().splitlines()

  state = parse_input(input_lines)
  result = execute(state)
  print(f"TEST Result: {result}")
  #assert result == ?
  #print(f"TEST PASSED!")

  # ACTUAL
  with open("./input/day?_actual.txt", "r") as text_file:
    input_lines = text_file.read().splitlines()

  state = parse_input(input_lines)
  result = execute(state)
  print(f"ACTUAL Result: {result}")
  #assert result == ?
  #print(f"ACTUAL PASSED!")
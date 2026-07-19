STARTING_POSITION = 50
DIAL_SIZE = 100

def move(position: int, direction: str, distance: int) -> tuple[int, int]:

    if direction == "L":
        final_position = position - distance
    elif direction == "R":
        final_position = position + distance
    else:
        raise ValueError(f"Unexpected direction: {direction}")

    passed_zero = final_position // DIAL_SIZE
    final_position = final_position % DIAL_SIZE

    if position != 0 and final_position == 0:
        passed_zero += 1

    return final_position, passed_zero

def execute(puzzle_input: list[str]) -> int:
    position = STARTING_POSITION
    total_passed_zero = 0

    for instruction in puzzle_input:
        direction = instruction[0]
        distance = int(instruction[1:])
        position, passed_zero = move(position, direction, distance)
        total_passed_zero += passed_zero

    return total_passed_zero

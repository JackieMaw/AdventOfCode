STARTING_POSITION = 50
DIAL_SIZE = 100


def move(position: int, direction: str, distance: int | str) -> int:
    distance = int(distance)

    if direction == "L":
        distance = -distance
    elif direction != "R":
        raise ValueError(f"Unexpected direction: {direction}")

    return (position + distance) % DIAL_SIZE


def execute(puzzle_input: list[str]) -> int:
    position = STARTING_POSITION
    zero_count = 0

    for instruction in puzzle_input:
        direction = instruction[0]
        distance = instruction[1:]
        position = move(position, direction, distance)

        if position == 0:
            zero_count += 1

    return zero_count

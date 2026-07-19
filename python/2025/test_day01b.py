import pytest

from utilities import get_expected_result, get_input, get_or_download_input, get_strings
from day01b import execute, move

@pytest.mark.parametrize(
    ("counter", "direction", "distance", "expected_position", "expected_passed_zero"),
    [
        (50, "L", 1, 49, 0),
        (50, "R", 1, 51, 0),
        (50, "R", 49, 99, 0),
        (50, "R", 50, 0, 1),
        (50, "L", 50, 0, 1),
        (50, "L", 51, 99, 1),
        (50, "R", 1000, 50, 10),
        (0, "R", 0, 0, 0),
        (0, "L", 0, 0, 0),
    ],
)
def test_move(counter, direction, distance, expected_position, expected_passed_zero):
    position, passed_zero = move(counter, direction, distance)
    assert position == expected_position
    assert passed_zero == expected_passed_zero

def test_move_rejects_unknown_direction():
    with pytest.raises(ValueError, match="Unexpected direction"):
        move(50, "X", 1)

YEAR = 2025
DAY = 1
PART = "b"

def test_sample_input():
    puzzle_input = get_strings(get_input(YEAR, DAY, "_test"))
    expected = get_expected_result(YEAR, DAY, PART, "_test")
    assert execute(puzzle_input) == expected

def test_full_input():
    puzzle_input = get_strings(get_or_download_input(YEAR, DAY))
    expected = get_expected_result(YEAR, DAY, PART)
    assert execute(puzzle_input) == expected

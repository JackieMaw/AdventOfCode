from utilities import *
import math
import copy

def get_hash(text):
    current_value = 0

    for c in text:
        assert ord(c) != 10
        current_value += ord(c)
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value

def remove_lense_from_box(box, lense_name_to_find):
    for lense in box:
        (lense_name, focal_length) = lense
        if lense_name == lense_name_to_find:
            box.remove(lense)
            return

def add_lense_to_box(box, lense_name_to_find, new_focal_length):
    modified_lense = (lense_name_to_find, new_focal_length)
    for lense_index, lense in list(enumerate(box)):
        (lense_name, focal_length) = lense
        if lense_name == lense_name_to_find:
            box[lense_index] = modified_lense
            return
    box.append(modified_lense)

def remove_lense(instruction, all_boxes):
    (lense_name, _) = instruction.split("-")
    lense_hash = get_hash(lense_name)
    box = all_boxes[lense_hash]
    remove_lense_from_box(box, lense_name)

def add_lense(instruction, all_boxes):
    (lense_name, new_focal_length) = instruction.split("=")
    lense_hash = get_hash(lense_name)
    box = all_boxes[lense_hash]
    add_lense_to_box(box, lense_name, int(new_focal_length))

def initialize_lenses(initialization_sequence):
    all_boxes = [ [] for _ in range(256) ]

    for instruction in initialization_sequence:
        if "-" in instruction:
            remove_lense(instruction, all_boxes)
        elif "=" in instruction:
            add_lense(instruction, all_boxes)
        else:
            raise Exception(f"Unexpected case for instruction: {instruction}")

    print(all_boxes)
    return all_boxes

def get_focus_power_of_lense(box_number, lense_position, focal_length):
    focus_power = box_number + 1
    focus_power = focus_power * (lense_position + 1) * focal_length
    return focus_power

def get_total_focus_power_of_box(box_number, lenses):
    total_focus_power = 0
    for lense_position, lense in enumerate(lenses):
        (lense_name, focal_length) = lense
        total_focus_power += get_focus_power_of_lense(box_number, lense_position, focal_length)
    return total_focus_power

def get_sum_of_focus_power(all_text):
    boxes = initialize_lenses(all_text)
    return sum(get_total_focus_power_of_box(box_number, lenses) for box_number, lenses in enumerate(boxes))

def execute(all_text):
    print(all_text)
    result = get_sum_of_focus_power(all_text)
    print(f"result: {result}")
    return result

# TESTS
assert get_hash("HASH") == 52
assert get_focus_power_of_lense(0, 0, 1) == 1
assert get_focus_power_of_lense(0, 1, 2) == 4
assert get_total_focus_power_of_box(0, [("rn", 1),("cm", 2)]) == 5

boxes = initialize_lenses("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(","))
assert boxes[0] == [('rn', 1), ('cm', 2)]
assert boxes[1] == []
assert boxes[2] == []
assert boxes[3] == [('ot', 7), ('ab', 5), ('pc', 6)]

print("UNIT TESTS PASSED")

assert execute("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")) == 145
print("INTEGRATION TESTS PASSED")

YEAR = 2023
DAY = 15

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input_lines = get_strings_csv(raw_input)
assert execute(input_lines) == 213097
print("ANSWER CORRECT")
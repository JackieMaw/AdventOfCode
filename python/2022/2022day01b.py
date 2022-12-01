from utilities import get_input

def execute(input):
    total_calories_per_elf = []
    total_calories = 0
    for calories_string in input:
        if calories_string == "":
            total_calories_per_elf.append(total_calories)
            total_calories = 0
        else:
            total_calories += int(calories_string)    
    total_calories_per_elf.append(total_calories)
    total_calories_per_elf.sort()
    top3 = total_calories_per_elf[-3:]
    result = sum(top3)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2022
DAY = 1

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 45000
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 200044
print("ANSWER CORRECT")
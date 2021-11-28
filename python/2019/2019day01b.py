from utilities import *
import math

def execute(input_data):
    sum = 0
    for mass in input_data:
        sum += fuel_required(mass)
    return sum

def fuel_required(mass):
    fuel_for_mass = math.floor(mass / 3) - 2
    #print (f"mass: {mass} => fuel_for_mass: {fuel_for_mass}")
    if (fuel_for_mass > 0):
        fuel_for_fuel = fuel_required(fuel_for_mass)
        #print (f"fuel: {fuel_for_mass} => fuel_for_fuel: {fuel_for_fuel}")
        return fuel_for_mass + fuel_for_fuel
    else:
        return 0

assert fuel_required(12) == 2
assert fuel_required(14) == 2
assert fuel_required(1969) == 966
assert fuel_required(100756) == 50346
print("ALL TESTS PASSED")

YEAR = 2019
DAY = 1
raw_input = get_or_download_input(YEAR, DAY)
input = get_integers(raw_input)
assert execute(input) == 4902650
print("ANSWER CORRECT")
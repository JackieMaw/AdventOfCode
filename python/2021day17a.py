#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

# On each step, these changes occur in the following order:
# The probe's x position increases by its x velocity.
# The probe's y position increases by its y velocity.
# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
# Due to gravity, the probe's y velocity decreases by 1.

def move_next(pos, velocity):
    (x, y) = pos
    (vx, vy) = velocity
    new_pos = (x + vx, y + vy)
    # because of drag, x movement is slowing down
    # because of gravity, y movement is slowing down if it's going up, or speeding up if it's going down 
    new_velocity = (vx - math.copysign(1, vx), vy - 1)
    #print(f"       MOVE - Position: {pos} => {new_pos}, Velocity: {velocity} => {new_velocity}")
    return new_pos, new_velocity

def hit_target(pos, target):
    (x, y) = pos
    ((x_min, x_max), (y_min, y_max)) = target
    in_range = x >= x_min and x <= x_max and y >= y_min and y <= y_max
    too_low = y < y_min
    too_wide = x > x_max
    missed = too_low or too_wide
    return in_range, missed

def will_hit_target(velocity, target):
    pos = (0, 0)
    (vx, vy) = velocity
    starting_velocity = velocity
    assert vx > 0
    while True:
        pos, velocity = move_next(pos, velocity)
        in_range, missed = hit_target(pos, target) 
        if in_range:
            print(f"HIT: velocity => {starting_velocity}")
            return True
        if missed: # no longer possible
            print(f"MISSED: velocity => {starting_velocity}")
            return False    

def execute(x_min, x_max, y_min, y_max):
    max_vy = 0

    target = ((x_min, x_max), (y_min, y_max))
    
    # pick initial velocity which hits the target in the first step, by firing down
    vx = x_min
    vy = y_max
    velocity = (vx, vy)
    print(f"Choose initial velocity {velocity} for target area: {target}")
    hit_target = will_hit_target(velocity, target)
    if hit_target and vy > max_vy:
        print(f"New max vy {max_vy}")
        max_vy = vy

    # since vy has a direct correlation to the max_height, 
    # increase vy until we miss 
    # then decrease vx until we hit
    # keep going while vx > 0

    while vx > 1:
        
        while hit_target: # keep increasing vy until we miss
            vy += 1
            print(f"...increasing vy to {vy}")
            velocity = (vx, vy)
            hit_target = will_hit_target(velocity, target)
            if hit_target and vy > max_vy:
                print(f"New max vy {max_vy}")
                max_vy = vy

        vx -= 1 # keep decreasing vx until we hit
        print(f"...decreasing vx to {vx}")
        velocity = (vx, vy)        
        hit_target = will_hit_target(velocity, target)
        if hit_target and vy > max_vy:
            print(f"New max vy {max_vy}")
            max_vy = vy

    result = max_vy * (max_vy + 1) / 2
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 17

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# target area: x=20..30, y=-10..-5
assert execute(20, 30, -10, -5) == 45 
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# target area: x=207..263, y=-115..-63
assert execute(207, 263, -115, -63) == 0
print("ANSWER CORRECT")
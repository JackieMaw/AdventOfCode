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
    vx = vx - abs(vx) / vx if vx != 0 else 0
    vy = vy - 1
    new_velocity = (vx, vy)
    # print(f"       MOVE - Position: {pos} => {new_pos}, Velocity: {velocity} => {new_velocity}")
    return new_pos, new_velocity

def check_hit_target(pos, target):
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
        in_range, missed = check_hit_target(pos, target) 
        if in_range:
            print(f"HIT: velocity => {starting_velocity}")
            return True
        if missed: # no longer possible
            #print(f"MISSED: velocity => {starting_velocity}")
            return False    

def get_good_vx(target):
    
    ((x_min, x_max), (y_min, y_max)) = target
    # find the vx which has a vx_sum within the target range of x:
    vx = 0
    missed = False
    while not missed:
        vx += 1
        vx_sum = vx * (vx + 1) / 2
        in_range = vx_sum >= x_min and vx_sum <= x_max
        missed = vx_sum > x_max
        if in_range:
            return vx

    return None


def execute(x_min, x_max, y_min, y_max):

    target = ((x_min, x_max), (y_min, y_max))

    min_vy = y_min
    max_vy = get_max_vy(target)
    min_vx = 1
    max_vx = x_max

    solutions = []

    print(f"Brute force all combinations for vx: {min_vx} => {max_vx} and vy {min_vy} => {max_vy}")

    for vx in range(min_vx, max_vx + 1):
        for vy in range(min_vy, max_vy + 1):
            velocity = (vx, vy)
            hit_target = will_hit_target(velocity, target)
            if hit_target:
                solutions.append(velocity)
    
    result = len(solutions)
    print(f"result: {result}") 
    return result

def get_max_vy(target):

    max_vy = 0
  
    # pick initial velocity which hits the target in the first step, by firing up
    vx = get_good_vx(target)
    # picking this vy means vx will be 0 by the time the ball comes back to 0
    vy = math.ceil(vx / 2)
    
    velocity = (vx, vy)
    print(f"Choose initial velocity {velocity} for target area: {target}")

    hit_target = will_hit_target(velocity, target)
    if hit_target and vy > max_vy:
        max_vy = vy
        #print(f"New max vy {max_vy}")

    # since vy has a direct correlation to the max_height, 
    # increase vy until we miss - will this ever happen?
    while hit_target: # keep increasing vy until we miss
        vy += 1
        # print(f"...increasing vy to {vy}")
        velocity = (vx, vy)
        hit_target = will_hit_target(velocity, target)
        if hit_target and vy > max_vy:
            max_vy = vy
            # print(f"New max vy {max_vy}")

    # try a few more times, just to see
    while vy < max_vy + 100:
        vy += 1
        # print(f"...increasing vy to {vy}")
        velocity = (vx, vy)
        hit_target = will_hit_target(velocity, target)
        if hit_target and vy > max_vy:
            max_vy = vy
            # print(f"New max vy {max_vy}")

    print(f"max_vy: {max_vy}") 
    return max_vy

# TESTS
assert get_good_vx(((20, 30), (-10, -5))) == 6
assert get_good_vx(((207, 263) , (-115, -63))) == 20
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 17

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# target area: x=20..30, y=-10..-5
assert execute(20, 30, -10, -5) == 112 
print("TEST INPUT PASSED")

# REAL INPUT DATA
# raw_input = get_or_download_input(YEAR, DAY)
# input = get_strings(raw_input)
# target area: x=207..263, y=-115..-63
assert execute(207, 263, -115, -63) == 4973
print("ANSWER CORRECT")
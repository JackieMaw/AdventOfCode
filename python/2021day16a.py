#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def get_bits(hex):
    bits = "{0:04b}".format(int(hex, 16))
    # print(f"{hex} => {bits}")
    return bits

def get_all_bits(message):
    bits = ""
    for char in message:
        bits += get_bits(char)
    print(f"{message} => {bits}")
    return bits

def process_bits(bits):
    ptr = 0
    total_version_sum = 0
    while ptr < len(bits):
        version_sum, ptr = parse_next_packet(bits, ptr)
        total_version_sum += version_sum
        padding = 16 - (ptr % 16)
        print(f"ptr: {ptr} needs padding => {padding}")
        ptr += padding
    return total_version_sum

def parse_literal(bits, ptr):
    
    start = ptr
    print(f"parse_literal @ {start}")

    allbits = ""
    signal_bit = bits[ptr : ptr + 1]        
    ptr += 1
    allbits += bits[ptr : ptr + 4]
    ptr += 4
    while signal_bit == 1: # keep going
        signal_bit = bits[ptr : ptr + 1]        
        ptr += 1
        allbits += bits[ptr : ptr + 4]
        ptr += 4

    val = int(allbits, 2)
    print(f"ptr: {start} => val: {val}")

    return val, ptr


def parse_operator(bits, ptr):

# If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
# If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

    total_version_sum = 0
    start = ptr
    print(f"parse_operator @ {start}")
    
    length_type_id = int(bits[ptr : ptr + 1], 2)
    ptr += 1

    if length_type_id == 0:
        total_length_in_bits = int(bits[ptr : ptr + 15], 2)
        print(f"ptr: {start} => length_type_id: {length_type_id}, total_length_in_bits: {total_length_in_bits}")
        ptr += 15

        version_sum = process_bits(bits[ptr : ptr + total_length_in_bits])
        ptr += total_length_in_bits
        total_version_sum += version_sum

    elif length_type_id == 1:
        number_of_subpackets = int(bits[ptr : ptr + 11], 2)
        print(f"ptr: {start} => length_type_id: {length_type_id}, number_of_subpackets: {number_of_subpackets}")
        ptr += 11

        subpacket_count = 0
        while subpacket_count < number_of_subpackets:
            version_sum, ptr = parse_next_packet(bits, ptr)
            total_version_sum += version_sum
            subpacket_count += 1

    return total_version_sum, ptr

def parse_next_packet(bits, ptr):

# Every packet begins with a standard header: 
# the first three bits encode the packet version, 
# and the next three bits encode the packet type ID.

    total_version_sum = 0
    start = ptr

    packet_version = int(bits[ptr : ptr + 3], 2)
    ptr += 3
    packet_type_id = int(bits[ptr : ptr + 3], 2)
    ptr += 3

    print(f"ptr: {start} => packet_version: {packet_version}, packet_type_id: {packet_type_id}")
    total_version_sum += packet_version

    if packet_type_id == 4: # literal value
        version_sum, ptr = parse_literal(bits, ptr)
        total_version_sum += version_sum
    else:
        version_sum, ptr = parse_operator(bits, ptr)
        total_version_sum += version_sum

    return total_version_sum, ptr

def execute(input):
    bits = get_all_bits(input)
    result = process_bits(bits)
    print(f"result: {result}") 
    return result

# TESTS
assert get_all_bits("D2FE28") == "110100101111111000101000"

assert process_bits("11010001010") == 1 # literal 10
assert process_bits("01010010001001000000000") == 1 # literal 20
assert process_bits("010100100010010000000000000000") == 1 # literal 20 with extra padding
assert process_bits("1101000101001010010001001000000000") == 1 # literal 10, literal 20 with extra padding
assert execute("38006F45291200") == 16

assert execute("EE00D40C823060") == 16 # literal 1, literal 2, literal 3

assert execute("8A004A801A8002F478") == 16
assert execute("620080001611562C8802118E34") == 16
assert execute("8A004A8C0015000016115A2E0802F18234001A8002F478") == 16
assert execute("A0016C880162017C3686B18A3D4780") == 16
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 16

# TEST INPUT DATA
# raw_input = get_input(YEAR, DAY, "_test")
# input = get_strings(raw_input)
# assert execute(input) == 0
# print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
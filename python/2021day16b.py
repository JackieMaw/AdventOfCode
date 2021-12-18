#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy
from functools import reduce
import operator

def get_bits(hex):
    # bits = "{0:04b}".format(int(hex, 16))

    hexaDict = {}
    hexaDict['0'] = '0000'
    hexaDict['1'] = '0001'
    hexaDict['2'] = '0010'
    hexaDict['3'] = '0011'
    hexaDict['4'] = '0100'
    hexaDict['5'] = '0101'
    hexaDict['6'] = '0110'
    hexaDict['7'] = '0111'
    hexaDict['8'] = '1000'
    hexaDict['9'] = '1001'
    hexaDict['A'] = '1010'
    hexaDict['B'] = '1011'
    hexaDict['C'] = '1100'
    hexaDict['D'] = '1101'
    hexaDict['E'] = '1110'
    hexaDict['F'] = '1111'

    bits = hex
    for key in hexaDict.keys():
        bits = bits.replace(key, hexaDict.get(key))

    return bits

def get_all_bits(message):
    bits = ""
    for char in message:
        bits += get_bits(char)
    #print(f"{message} => {bits}")
    return bits

def evaluate_bits(bits, with_padding = True):
    #print()
    #print(f"process_bits: {bits}")
    #print()
    ptr = 0
    all_values = []
    while ptr < len(bits): 
        value, ptr = evaluate_packet(bits, ptr)
        all_values.append(value)
        if with_padding and ptr % 8 != 0:
            padding = 8 - (ptr % 8)
            #print(f"ptr: {ptr} needs padding => {padding}")
            ptr += padding
    print(f"all_values: {all_values}")
    return all_values

def evaluate_literal(bits, ptr):
    
    start = ptr
    #print(f"parse_literal @ {start}")

    allbits = ""
    signal_bit = bits[ptr : ptr + 1]        
    ptr += 1
    allbits += bits[ptr : ptr + 4]
    ptr += 4
    while signal_bit == '1': # keep going
        signal_bit = bits[ptr : ptr + 1]        
        ptr += 1
        allbits += bits[ptr : ptr + 4]
        ptr += 4

    value = int(allbits, 2)
    #print(f"ptr: {start} => val: {val}")

    return value, ptr


def evaluate_operator(packet_type_id, bits, ptr):

# If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
# If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

    parameter_all_values = []
    start = ptr
    #print(f"parse_operator @ {start}")
    
    length_type_id = int(bits[ptr : ptr + 1], 2)
    ptr += 1

    if length_type_id == 0:
        total_length_in_bits = int(bits[ptr : ptr + 15], 2)
        print(f"[{start} of {len(bits)}]     ({total_length_in_bits} bits)")
        assert ptr + total_length_in_bits <= len(bits)
        #print(f"ptr: {start} => length_type_id: {length_type_id}, total_length_in_bits: {total_length_in_bits}")
        ptr += 15

        parameter_all_values = evaluate_bits(bits[ptr : ptr + total_length_in_bits], with_padding=False)
        ptr += total_length_in_bits

    elif length_type_id == 1:
        number_of_subpackets = int(bits[ptr : ptr + 11], 2)
        print(f"[{start} of {len(bits)}]     ({number_of_subpackets} subpackets)")
        #print(f"ptr: {start} => length_type_id: {length_type_id}, number_of_subpackets: {number_of_subpackets}")
        ptr += 11

        subpacket_count = 0
        while subpacket_count < number_of_subpackets:
            value, ptr = evaluate_packet(bits, ptr)
            parameter_all_values.append(value)
            subpacket_count += 1


# Packets with type ID 0 are sum packets - their value is the sum of the all_values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 1 are product packets - their value is the result of multiplying together the all_values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
# Packets with type ID 2 are minimum packets - their value is the minimum of the all_values of their sub-packets.
# Packets with type ID 3 are maximum packets - their value is the maximum of the all_values of their sub-packets.
# Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
# Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

    value = None
    if packet_type_id == 0: #sum
        value = sum(parameter_all_values)
    elif packet_type_id == 1: #product
        value = reduce(operator.mul, parameter_all_values, 1)
    elif packet_type_id == 2: #min
        value = min(parameter_all_values)
    elif packet_type_id == 3: #max
        value = max(parameter_all_values)
    elif packet_type_id == 5: #>
        value = 1 if parameter_all_values[0] > parameter_all_values[1] else 0
    elif packet_type_id == 6: #<
        value = 1 if parameter_all_values[0] < parameter_all_values[1] else 0
    elif packet_type_id == 7: #==
        value = 1 if parameter_all_values[0] == parameter_all_values[1] else 0

    return value, ptr

def evaluate_packet(bits, ptr):

# Every packet begins with a standard header: 
# the first three bits encode the packet version, 
# and the next three bits encode the packet type ID.

    value = None
    start = ptr

    packet_version = int(bits[ptr : ptr + 3], 2)
    ptr += 3
    packet_type_id = int(bits[ptr : ptr + 3], 2)
    ptr += 3

    # print(f"ptr: {start} => packet_version: {packet_version}, packet_type_id: {packet_type_id}")

    if packet_type_id == 4: # literal value
        value, ptr = evaluate_literal(bits, ptr)        
        print(f"[{start} of {len(bits)}] LITERAL = {value}      <version {packet_version}>")
    else: # operator    
        print(f"[{start} of {len(bits)}] OPERATOR = {packet_type_id}      <version {packet_version}>")
        value, ptr = evaluate_operator(packet_type_id, bits, ptr)

    return value, ptr

def execute(input):
    bits = get_all_bits(input)
    all_values = evaluate_bits(bits)
    # at the outer level there should be only one packet
    assert len(all_values) == 1
    result = all_values[0]
    print(f"result: {result}") 
    return result

# TESTS
# C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
assert execute("C200B40A82") == 3
# 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
assert execute("04005AC33890") == 54
# 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
assert execute("880086C3E88112") == 7
# CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
assert execute("CE00C43D881120") == 9
# D8005AC2A8F0 produces 1, because 5 is less than 15.
assert execute("D8005AC2A8F0") == 1
# F600BC2D8F produces 0, because 5 is not greater than 15.
assert execute("F600BC2D8F") == 0
# 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
assert execute("9C005AC2F8F0") == 0
# 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
assert execute("9C0141080250320F1802104A08") == 1

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
assert execute(input) == 912901337844
print("ANSWER CORRECT")
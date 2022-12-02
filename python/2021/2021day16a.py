#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy

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

def process_bits(bits, with_padding = True):
    #print()
    #print(f"process_bits: {bits}")
    #print()
    ptr = 0
    total_version_sum = 0
    while ptr < len(bits):
        version_sum, ptr = parse_next_packet(bits, ptr)
        total_version_sum += version_sum
        if with_padding and ptr % 8 != 0:
            padding = 8 - (ptr % 8)
            #print(f"ptr: {ptr} needs padding => {padding}")
            ptr += padding
    #print(f"total_version_sum: {total_version_sum}")
    return total_version_sum

def parse_literal(bits, ptr):
    
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

    val = int(allbits, 2)
    #print(f"ptr: {start} => val: {val}")

    return val, ptr


def parse_operator(bits, ptr):

# If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
# If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

    total_version_sum = 0
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

        version_sum = process_bits(bits[ptr : ptr + total_length_in_bits], with_padding=False)
        ptr += total_length_in_bits
        total_version_sum += version_sum

    elif length_type_id == 1:
        number_of_subpackets = int(bits[ptr : ptr + 11], 2)
        print(f"[{start} of {len(bits)}]     ({number_of_subpackets} subpackets)")
        #print(f"ptr: {start} => length_type_id: {length_type_id}, number_of_subpackets: {number_of_subpackets}")
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

    # print(f"ptr: {start} => packet_version: {packet_version}, packet_type_id: {packet_type_id}")
    total_version_sum += packet_version

    if packet_type_id == 4: # literal value
        val, ptr = parse_literal(bits, ptr)        
        print(f"[{start} of {len(bits)}] LITERAL = {val}      <version {packet_version}>")
    else: # operator    
        print(f"[{start} of {len(bits)}] OPERATOR = {packet_type_id}      <version {packet_version}>")
        version_sum, ptr = parse_operator(bits, ptr)
        total_version_sum += version_sum

    return total_version_sum, ptr

def execute(input):
    bits = get_all_bits(input)
    result = process_bits(bits)
    print(f"result: {result}") 
    return result

# TESTS
#assert get_all_bits("D2FE28") == "110100101111111000101000"
#assert process_bits("110100101111111000101000") == 6 # literal 2021

#assert process_bits("11010001010") == 6 # literal 10
#assert process_bits("01010010001001000000000") == 1 # literal 20
#assert process_bits("010100100010010000000000000000") == 1 # literal 20 with extra padding
#assert process_bits("1101000101001010010001001000000000") == 1 # literal 10, literal 20 with extra padding

# For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:
# 00111000000000000110111101000101001010010001001000000000
# VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
# The three bits labeled V (001) are the packet version, 1.
# The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
# The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
# The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
# The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
# The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.
# After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.
# assert execute("38006F45291200") == 9 # operator => literal 10, literal 20

# As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:
# 11101110000000001101010000001100100000100011000001100000
# VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
# The three bits labeled V (111) are the packet version, 7.
# The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
# The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
# The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
# The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
# The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
# The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.
# After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.
# assert execute("EE00D40C823060") == 14 # operator => literal 1, literal 2, literal 3

# 8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
# assert execute("8A004A801A8002F478") == 16
# 620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
# assert execute("620080001611562C8802118E34") == 12
# C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
# assert execute("C0015000016115A2E0802F182340") == 23
# A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.
# assert execute("A0016C880162017C3686B18A3D4780") == 31

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
assert execute(input) == 934
print("ANSWER CORRECT")
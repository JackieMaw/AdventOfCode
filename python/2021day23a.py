#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy


team_map = {"A" : 0, "B" : 1, "C" : 2, "D" : 3} 
team_number_map = ["A", "B", "C", "D"]

def get_players(input_data):

    players = [ [] for _ in range(4) ]

    width = len(input_data[0])
    length = len(input_data)

    for x in range(width):
        for y in range(length):
            player = input_data[y][x]
            if player in team_map:
                index = team_map[player]
                players[index].append((x, y))

    print(players)

    return players

final_state = [[(3, 2), (3, 3)], [(5, 2), (5, 3)], [(7, 2), (7, 3)], [(9, 2), (9, 3)]]
hallway = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1)]

def get_settled(state):
    return []

moves_cache = {}

def get_moves_from_cache(start, end):
    if (start, end) in moves_cache:
        return moves_cache[(start, end)]
    moves = get_moves(start, end)
    moves_cache[(start, end)] = moves
    return moves

def get_moves(start, end):
    # try to move to the destination one step at a time
    (start_x, start_y) = start
    (end_x, end_y) = end

    #print(f"  Try move from {start} to {end} ==>")

    # MOVES CAN BE CACHED, there are only 19 x 19 possible combinations

    # first move up to the hallway from start_y to 1
    moves = [(start_x, y) for y in range(start_y - 1, 0, -1)]

    # then move across the hallway from start_x to end_x
    if start_x < end_x:
        moves.extend([(x, 1) for x in range(start_x + 1, end_x)])
    elif start_x > end_x:
        moves.extend([(x, 1) for x in range(start_x - 1, end_x, -1)])

    # then move down into the room from 1 to end_y
    moves.extend([(end_x, y) for y in range(1, end_y)])

    return moves

def try_move_to(start, end, state, player_cost):
    
    players = [player for team_state in state for player in team_state]

    # check if the destination is free
    if end in players:
        #print(f"  Cannot move from {start} to {end} because another player is already there.")
        return None

    moves = get_moves(start, end)    

    for move in moves:
        if move in players:
            #print(f"     Checking {move}... BLOCKED")
            return None
        #else:        
            #print(f"     Checking {move}... OK")

    return (len(moves) + 1) * player_cost

def get_possible_moves(state):

    # players = list of locations for A, B, C, D players
    #players = [[(5, 2), (5, 3)], [(3, 3), (7, 3)], [(3, 2), (9, 3)], [(7, 2), (9, 2)]]

    possible_moves = []
    settled = get_settled(state)

    for team_number in range(4):
        team_state = state[team_number]
        team_name = team_number_map[team_number]

        for player in team_state:
            
            print(f"Computing all possible moves for {team_name} @ {player}:")

            # if the player is already home it will not move again
            if player not in settled:

                player_cost = 10 ** team_number

                # try to move home 
                home_room = final_state[team_number]
                for home_space in home_room:
                    cost = try_move_to(player, home_space, state, player_cost)
                    if cost is not None:
                        # TODO - also check no foreigners are in the room!
                        possible_moves.append((player, home_space, cost))       
                        print(f"*** {team_name} can move from {player} to {home_space} [HOME] with cost {cost}")
                        # if you can move home, then all other moves are WORSE
                        # return possible_moves    

                # if you are not in the hallway already, try to move into hallway
                if player not in hallway:
                    for hallway_space in hallway:
                        cost = try_move_to(player, hallway_space, state, player_cost)
                        if cost is not None:
                            possible_moves.append((player, hallway_space, cost))
                            print(f"*** {team_name} can move from {player} to {hallway_space} [HALLWAY] with cost {cost}")

    return possible_moves

def execute(input_data):
    print(input_data)

    players = get_players(input_data)
    possible_moves = get_possible_moves(players)

    result = len(possible_moves)
    print(f"result: {result}") 
    return result

# TESTS
# assert execute(get_strings_csv(["ABCD"])) == 0
# print("ALL TESTS PASSED")

YEAR = 2021
DAY = 23

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 12521
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 0
print("ANSWER CORRECT")
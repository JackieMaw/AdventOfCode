#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities.utilities import *
import math
import copy
import heapq

team_map = {"A" : 0, "B" : 1, "C" : 2, "D" : 3} 
team_number_map = ["A", "B", "C", "D"]

def get_initial_state(input_data):

    state = [ [] for _ in range(4) ]

    width = len(input_data[0])
    length = len(input_data)

    for x in range(width):
        for y in range(length):
            player = input_data[y][x]
            if player in team_map:
                index = team_map[player]
                state[index].append((x, y))

    for team_state in state:
        team_state.sort(key = lambda player: player[1])

    print(state)

    return state

final_state = [[(3, 2), (3, 3)], [(5, 2), (5, 3)], [(7, 2), (7, 3)], [(9, 2), (9, 3)]]
hallway = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1)]

def to_state_string(state):
    return "#".join(["|".join([str(player) for player in team_state]) for team_state in state])

def from_state_string(state_string):        
    # state = []

    # for team_state_string in state_string.split("#"):
    #     team_state = []
    #     for player_state_string in team_state_string.split("|"):
    #         player_state = eval(player_state_string)
    #         team_state.append(player_state)
    #     state.append(team_state)

    # return state    
    return [[eval(player_state_string) for player_state_string in team_state_string.split("|")] for team_state_string in state_string.split("#")]


def is_foreigner_present(state, team_number, team_room_spaces, player):

    team_players = state[team_number]

    (player_x, player_y) = player
    for team_room_space in team_room_spaces:
        (x, y) = team_room_space
        # deeper in the room than the player
        if y > player_y: 
            # this space should be occupied by someone in my team
            if team_room_space not in team_players:
                return True
    
    return False

def is_settled(player, team_number, state):

    # to be settled, the player should be in the team room, and there should be no other foreign players deeper in the room
    team_room_spaces = final_state[team_number]
    if player in team_room_spaces:
        if is_foreigner_present(state, team_number, team_room_spaces, player):
            return False
        else:
            return True

    return False

def get_all_settled(state):

    settled = []

    for team_number in range(4):
        team_state = state[team_number]
        for player in team_state:            
            if is_settled(player, team_number, state):
                settled.append(player)

    return settled

moves_cache = {}

def get_moves_from_cache(start, end):
    if (start, end) in moves_cache:
        return moves_cache[(start, end)]
    moves = get_moves(start, end)
    moves_cache[(start, end)] = moves
    return moves

def get_moves(start, end):
    
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

    # try to move to the destination one step at a time
    moves = get_moves_from_cache(start, end) 

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
    settled = get_all_settled(state)

    for team_number in range(4):
        team_state = state[team_number]
        team_name = team_number_map[team_number]

        for player in team_state:
            
            #print(f"Computing all possible moves for {team_name} @ {player}:")

            # if the player is already home it will not move again
            # if player in settled:
            #     print(f"    {team_name} @ {player} IS SETTLED")
            # else:

            if player not in settled:

                player_cost = 10 ** team_number

                # try to move home 
                home_room = final_state[team_number]
                for home_space in reversed(home_room): # try the lowest space first
                    cost = try_move_to(player, home_space, state, player_cost)
                    if cost is not None:
                        if not is_foreigner_present(state, team_number, home_room, home_space):
                            #print(f"*** {team_name} can move from {player} to {home_space} [HOME] with cost {cost}")
                            #possible_moves.append((player, home_space, cost))                            
                            # if you can move home into the lowest space, then all other moves are WORSE so abandon them
                            return [(player, home_space, cost)]   

                # if you are not in the hallway already, try to move into hallway
                if player not in hallway:
                    for hallway_space in hallway:
                        cost = try_move_to(player, hallway_space, state, player_cost)
                        if cost is not None:
                            possible_moves.append((player, hallway_space, cost))
                            #print(f"*** {team_name} can move from {player} to {hallway_space} [HALLWAY] with cost {cost}")

    return possible_moves

def apply_move(current_state, start, end):

    new_state = []

    for team_state in current_state:
        new_team_state = [end if player == start else player for player in team_state]
        new_team_state.sort(key = lambda player: player[1])
        new_state.append(new_team_state)

    return new_state

def get_shortest_path(initial_state):

    shortest_path = { to_state_string(initial_state) : 0 }
    visited = set()

    priority_queue = [(0, initial_state)]

    while len(priority_queue) > 0:
        #print(f"Visited: {len(visited)}")
        (cost_to_current_state, current_state) = heapq.heappop(priority_queue)
        current_state_string = to_state_string(current_state)
        visited.add(current_state_string)
        # list of (start, end, cost)
        possible_moves = get_possible_moves(current_state)
        for (start, end, cost_of_move) in possible_moves:
            new_state = apply_move(current_state, start, end)  
            new_state_string = to_state_string(new_state)          
            existing_cost_to_new_state = shortest_path[new_state_string] if new_state_string in shortest_path else None
            new_distance_to_new_state = cost_to_current_state + cost_of_move
            if existing_cost_to_new_state is None or new_distance_to_new_state < existing_cost_to_new_state:
                #print(f"    found shortest path to {(nx, ny)} : {new_distance_to_neighbour}")
                shortest_path[new_state_string] = new_distance_to_new_state
                # do not add if already visited
                if new_state_string not in visited:
                    heapq.heappush(priority_queue, (new_distance_to_new_state, new_state))

    final_state_string = to_state_string(final_state)
    return shortest_path[final_state_string]

def execute(input_data):
    print(input_data)

    state = get_initial_state(input_data)
    cost = get_shortest_path(state)

    result = cost
    print(f"result: {result}") 
    return result

# TESTS
assert to_state_string(final_state) == "(3, 2)|(3, 3)#(5, 2)|(5, 3)#(7, 2)|(7, 3)#(9, 2)|(9, 3)"
assert final_state == from_state_string("(3, 2)|(3, 3)#(5, 2)|(5, 3)#(7, 2)|(7, 3)#(9, 2)|(9, 3)")
print("ALL TESTS PASSED")

YEAR = 2021
DAY = 23

# TEST INPUT DATA

raw_input = get_input(YEAR, DAY, "_final")
input = get_strings(raw_input)
assert execute(input) == 0
print("TEST INPUT PASSED - FINAL STATE")

raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 12521
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 10526
print("ANSWER CORRECT")
#TODO - how to share utilities across folders? do I need to make a package?
from os import execl
from utilities import *
import math
import copy

def play(numbers, boards):
    last_winner = None
    for num in numbers:
        remove_boards = []
        for (i, (board, marked)) in enumerate(boards):
            i_won = mark(board, marked, num)
            if i_won:
                #print(f"i won! {i} with the number {num}")
                last_winner = (board, marked, num)
                remove_boards.append((board, marked))
        for board in remove_boards:
            boards.remove(board)
    return last_winner

def mark(board, marked, num):
    for i in range (0,5):
        for j in range (0,5):            
            if board[i][j] == num:
                marked[i][j] = 1
                return did_i_win(marked)
    return False

def did_i_win(marked):
    #check all rows
    for i in range (0,5):
        all_marked = True
        for j in range (0,5):     
            if not marked[i][j]:     
                all_marked = False  
        if all_marked:
            return True

    #check all columns
    for j in range (0,5):
        all_marked = True
        for i in range (0,5):     
            if not marked[i][j]:     
                all_marked = False  
        if all_marked:
            return True

    return False

def get_score(board, marked):
    sum = 0
    for i in range (0,5):
        for j in range (0,5):
            if not marked[i][j]:
                sum += int(board[i][j])
    return sum

def read_boards(input):
    boards = []
    this_board = None
    marked = None
    row_counter = 2
    while row_counter < len(input):
        line = input[row_counter].split()
        if len(line) == 5:
            if this_board is None:
                this_board = []      
                marked = []           
            this_board.append(line)
            marked.append([0,0,0,0,0])
            if len(this_board) == 5:
                boards.append((this_board, marked))
                this_board = None
                marked = None
        row_counter += 1   
    return boards

def execute(input):

    numbers = input[0].split(",")

    boards = read_boards(input) 

    (board, marked, num) = play(numbers, boards)

    score = get_score(board, marked) 
    print(f"score: {score}") 
    print(f"num: {num}") 
    result = score * int(num)
    print(f"result: {result}") 
    return result

YEAR = 2021
DAY = 4

# TEST INPUT DATA
raw_input = get_input(YEAR, DAY, "_test")
input = get_strings(raw_input)
assert execute(input) == 1924
print("TEST INPUT PASSED")

# REAL INPUT DATA
raw_input = get_or_download_input(YEAR, DAY)
input = get_strings(raw_input)
assert execute(input) == 8224
print("ANSWER CORRECT")
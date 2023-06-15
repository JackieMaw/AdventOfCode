#https://adventofcode.com/2019/day/17
#--- Day 17: Set and Forget ---

def is_scaffold_or_robot(char):
    return char in ("#", "^", ">", "<", "v")

def is_intersection_point(view, row_counter, col_counter):
    point = view[row_counter][col_counter]
    if is_scaffold_or_robot(point):
        above = view[row_counter-1][col_counter]
        below = view[row_counter+1][col_counter]
        left = view[row_counter][col_counter-1]
        right = view[row_counter][col_counter+1]
        if is_scaffold_or_robot(above) and is_scaffold_or_robot(below) and is_scaffold_or_robot(left) and is_scaffold_or_robot(right):
            return True
    return False

def get_alignment_paramter(row_counter, col_counter):
    return row_counter * col_counter

class VaccumRobot():
    
    def __init__(self, view):
        self.view = view    
        self.num_rows = len(view)
        self.num_cols = len(view[0])

    def get_alignment_parameters(self):

        sum_of_alignment_parameters = 0

        # intersections can never be on the edges so we skip the first and last rows and columns
        for row_counter in range(1, self.num_rows - 1):
            for col_counter in range(1, self.num_cols - 1):
                if is_intersection_point(self.view, row_counter, col_counter):
                    sum_of_alignment_parameters += get_alignment_paramter(row_counter, col_counter)
        
        return sum_of_alignment_parameters



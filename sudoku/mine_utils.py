from utils import *

def cross(a, b):
    return [s + t for s in a for t in b]

def grid_values(board):
    rows = "ABCDEFGHI"
    cols = "123456789"
    coords = cross(rows, cols)
    grid = {}
    
    for (a,b) in zip(coords, board):
        if(b != '.'):
            grid[a] = b
        else:
            grid[a] = cols
    
    return grid
    
def eliminate(grid):
    
    unitlist = [row_units, cols_units, square_units]
    ngrid = dict((a, b) for (a,b) in grid.items())
    
    for (a, c) in grid.items():
        for e in unitlist:
            for b in e:
                if a in b:
                    for d in b:
                        if(len(ngrid[d]) == 1 and d != a):
                            grid[a] = grid[a].replace(ngrid[d], "")
    
    return grid

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# OBS: had to lookup for the aswer
# Annotation: the usage of the one unique list for everything seems to be a lot
# more efficient
'''
 Algorithm analysis:
 goes at every set of lines, them at every set of columns and them every set of
 squares working at every number, looking for the ocurrency of them into the 
 grid, and collecting the positions where the elements seems to have only one
 ocurrency
'''
def only_choice(grid):
    nums = "123456789"
    
    for unit in unitlist:
        for n in nums:
            lst = [element for element in unit if n in grid[element]]
            if len(lst) == 1: # only one ocurrency
                grid[lst[0]] = n
    
    return grid
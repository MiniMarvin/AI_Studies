from utils import *
################################################################################
## Functions ###################################################################
def search(values):
    values = reduce_puzzle(values)
    
    if values == False:
        return {}
    
    res = [[a, b] for a, b in values.items() if len(b) == 1]
    if len(res) == 81: # size of the board
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    for i in range(2, 10):
        valid = [[a, b] for a, b in values.items() if len(b) == i]
        if len(valid) == 0:
            continue
        
        valid = valid[0]
        
        # works in the first valid element
        for number in valid[1]:
            grid = dict(values)
            grid[valid[0]] = number
            
            result = search(grid)
            if len(result) != 0:
                return result
        break
    
    return {}

################################################################################
## Script ######################################################################

# bd = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
# bd = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
bd = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
rows = "ABCDEFGHI"
cols = "123456789"

grid = grid_values(bd)

display(grid)

grid = search(grid)
print("\n\n")
try:
    display(grid)
except:
    print(grid)


print(d1)
print(d2)
from gamestate import *

def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    lst = gameState.get_legal_moves()

    if(len(lst) == 0):
        return True
    
    return False


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    val = gameState.actual_turn*2 - 1
    
    if terminal_test(gameState):
        return -val
    
    moves = gameState.get_legal_moves()
    vals = [max_value(gameState.forecast_move(a)) for a in moves]
    
    val = min(vals)
    
    return val


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    val = gameState.actual_turn*2 - 1
    
    if terminal_test(gameState):
        return -val
    
    moves = gameState.get_legal_moves()
    vals = [min_value(gameState.forecast_move(a)) for a in moves]
    
    val = max(vals)
    
    return val

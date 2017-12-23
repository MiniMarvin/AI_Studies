from gamestate import *

# a = GameState()
# a.print_actual_state()
# print(a.get_legal_moves())

def apply_moves(move_lst):
    bd = GameState()
    print("initial:")
    bd.print_actual_state()
    print(bd.get_legal_moves())
    
    for x in move_lst:
        print("Applied {}: {}".format(x, bd.actual_pos))
        bd = bd.forecast_move(x)
        bd.print_actual_state()
        print(bd.get_legal_moves())
        print("\n")

apply_moves([(0,0), (1,1)])
apply_moves([(0,0), (1,0)])

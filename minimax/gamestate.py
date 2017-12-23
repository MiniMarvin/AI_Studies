class GameState:
    actual_pos = [(None, None) for a in range(2)]
    bd = [["." for x in range(2)] for i in range(3)]
    actual_turn = 0
    r = 0
    c = 0

    def __init__(self, board = None, player = None, my_move = None, oponnent_move = None):
        if board == None:
            self.actual_pos = [(None, None) for a in range(2)]
            self.bd = [["." for x in range(2)] for i in range(3)]
            self.bd[2][1] = "#"
            self.r = 2
            self.c = 3
            self.actual_turn = 0
        else:
            self.r = 2
            self.c = 3
            self.bd = board
            self.actual_turn = 1
            if player == 1:
                self.actual_turn = 0
            self.actual_pos[self.actual_turn] = my_move
            self.actual_pos[player] = oponnent_move
        pass
    
    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.
        
        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        
        legal_moves = self.get_legal_moves()
        nbd = self.bd
        
        if move in legal_moves:
            nbd[move[0]][move[1]] = "#"
        else:
            return self
        
        p = 0
        if self.actual_turn == 0:
            p = 1
        
        return GameState(nbd, self.actual_turn, self.actual_pos[p], move)
    
    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        act_row = self.actual_pos[self.actual_turn][0]
        act_col = self.actual_pos[self.actual_turn][1]
        
        legal_moves = []
        
        if self.actual_pos[self.actual_turn] == (None, None):
            legal_moves = [(a, b) for a in range(3) for b in range(2) if self.bd[a][b] == "."]
            return legal_moves
        
        bd = self.bd
        
        # Iterate forward
        for a in range(act_col + 1, self.c - 1):
            if bd[a][act_row] != ".":
                break
            legal_moves += [(a, act_row)]
            
        for a in range(act_row + 1, self.r - 1):
            if bd[act_col][a] != "." and a != act_row:
                break
            legal_moves += [(act_col, a)]
        
        #iters backwards
        for a in range(act_col - 1, 0, -1):
            if bd[a][act_row] != "." and a != act_col:
                break
            legal_moves += [(a, act_row)]
            
        for a in range(act_row - 1, 0, -1):
            if bd[act_col][a] != "." and a != act_row:
                break
            legal_moves += [(act_col, a)]
        
        sums = [(1,1), (1, -1), (-1, -1), (-1, 1)]
        diags = [(act_col + a, act_row + b) for a, b in sums if 0 <= act_col + a < self.c and 0 <= act_row + b < self.r]
        legal_moves += [a for a in diags if bd[a[0]][a[1]] == "."]
        
        return legal_moves
    
    def print_actual_state(self):
        for i in self.bd:
            print(i)
        pass
"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    val = 0.0
    pdg = 0.0
    odg = 0.0
    
    # The difference of the squared sum of the degree of the next squares for both players
    if player == game.active_player:
        opponent = game.inactive_player
        player_moves = game.get_legal_moves()
        
        ct = len(player_moves)
        
        for move in player_moves:
            bd = game.forecast_move(move)
            pdg += len(bd.get_legal_moves(player))**4
            opponent_moves = game.get_legal_moves(opponent)
            for mv in opponent_moves:
                odg += len(bd.get_legal_moves(opponent))**4

        odg /= float(ct)

    else:
        opponent = game.active_player
        opponent_moves = game.get_legal_moves()
        pdg = 0
        odg = 0
        ct = len(opponent_moves)
        
        for move in opponent_moves:
            bd = game.forecast_move(move)
            odg += len(bd.get_legal_moves(opponent))**4
            player_moves = game.get_legal_moves(player)
            for mv in player_moves:
                odg += len(bd.get_legal_moves(player))**4

        pdg /= float(ct)

    val = float(pdg) - float(odg)

    return val


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")
    # sum of the square degrees of my opponnet move - the squared degree of my move
    val = 0
    pmul = 1
    omul = 1

    opponent = game.get_opponent(player)

    pdg = len(game.get_legal_moves(player))**2
    odg = len(game.get_legal_moves(opponent))**2
    val = pdg - odg

    # return len(game.get_legal_moves(player)) + 1 - len(game.get_legal_moves(game.get_opponent(player)))
    return val


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Implements the Warnsdorf's rule for knight's tour
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")
    # sum of the square degrees of my opponnet move - the squared degree of my move
    val = 0
    pmul = 1
    omul = 1

    opponent = game.get_opponent(player)

    pdg = len(game.get_legal_moves(player))**4
    odg = len(game.get_legal_moves(opponent))**4
    val = pdg - odg

    # return len(game.get_legal_moves(player)) + 1 - len(game.get_legal_moves(game.get_opponent(player)))
    return val

    return val


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)

        for ct in range(1, 100):
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.minimax(game, ct)

            except SearchTimeout:
                return best_move
                pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        best_move = (-1,-1) # defines for being able to return if no answer has been found
        self.player_agent = game.active_player

        valid_moves = game.get_legal_moves()
        eval_moves = [(self.min_search(game.forecast_move(move), depth - 1), move) for move in valid_moves]
        
        try:
            best_move = max(eval_moves)[1]
        except ValueError:
            pass

        # raise NotImplementedError
        return best_move
    
    def min_search(self, game, depth):
        """
        " Search the min level
        """
        #if the time have been passed raise an error
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # if the game ended just return the result
        if game.is_winner(self.player_agent) or game.is_loser(self.player_agent):
            return game.utility(self.player_agent)
        
        # if reached the max depth just returns the evaluation
        if(depth <= 0):
            return self.score(game, self.player_agent)
        
        # if is in the middle of the game them call the next helper
        valid_moves = game.get_legal_moves()
        
        move_list = [self.max_search(game.forecast_move(move), depth - 1) for move in valid_moves]
        
        return min(move_list)
    
    def max_search(self, game, depth):
        """
        " Search in the max level
        """
        #if the time have been passed raise an error
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # if the game ended just return the result
        if game.is_winner(self.player_agent) or game.is_loser(self.player_agent):
            return game.utility(self.player_agent)
        
        # if reached the max depth just returns the evaluation
        if(depth <= 0):
            return self.score(game, self.player_agent)
        
        # if is in the middle of the game them call the next helper
        valid_moves = game.get_legal_moves()
        
        move_list = [self.min_search(game.forecast_move(move), depth - 1) for move in valid_moves]
        
        return max(move_list)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        for ct in range(1, 100):
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, ct)

            except SearchTimeout:
                return best_move
                pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1,-1) # defines for being able to return if no answer has been found
        self.player_agent = game.active_player

        valid_moves = game.get_legal_moves()

        alpha = float("-inf")
        beta = float("inf")
        best_val = float("-inf")
        
        for move in valid_moves:
            next_state = game.forecast_move(move)
            val = self.min_search(next_state, depth - 1, alpha, beta)

            if val > best_val:
                best_val = val
                best_move = move

            alpha = max(alpha, val)
        
        return best_move

    #min node updates beta and max node updates alpha and if alpha > beta, prune
    def min_search(self, game, depth, alpha = float("-inf"), beta = float("inf")):
        """
        " Search the min level
        """
        #if the time have been passed raise an error
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # if the game ended just return the result
        if game.is_winner(self.player_agent) or game.is_loser(self.player_agent):
            return game.utility(self.player_agent)

        # if reached the max depth just returns the evaluation
        if depth <= 0:
            return self.score(game, self.player_agent)
        
        valid_moves = game.get_legal_moves()
        best_val = float("inf")

        for move in valid_moves:
            next_state = game.forecast_move(move)
            val = self.max_search(next_state, depth - 1, alpha, beta)
            
            if val <= alpha:
                return val

            best_val = min(best_val, val)
            beta = min(beta, val)

        return best_val
    
    #min node updates beta and max node updates alpha and if alpha > beta, prune
    def max_search(self, game, depth, alpha = float("-inf"), beta = float("inf")):
        """
        " Search in the max level
        """
        #if the time have been passed raise an error
        if self.time_left() < self.TIMER_THRESHOLD:
        # if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if the game ended just return the result
        if game.is_winner(self.player_agent) or game.is_loser(self.player_agent):
            return game.utility(self.player_agent)
        
        # if reached the max depth just returns the evaluation
        if depth <= 0:
            return self.score(game, self.player_agent)
        
        # if is in the middle of the game them call the next helper
        valid_moves = game.get_legal_moves()
        best_val = float("-inf")

        for move in valid_moves:
            next_state = game.forecast_move(move)
            val = self.min_search(next_state, depth - 1, alpha, beta)
            
            if val >= beta:
                return val
                
            best_val = max(best_val, val)
            alpha = max(alpha, val)

        return best_val

"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_win(self):
        self.player1 = "Player1"
        self.player2 = "Player2"
        little_game = isolation.Board(self.player1, self.player2, width=1, height=1)

        player = little_game.active_player
        opponent = little_game.inactive_player

        result = little_game.is_winner(player) or little_game.is_winner(opponent)
        self.assertFalse(result, "Found winner existing none!")
        
        little_game.apply_move((0,0))
        result = little_game.is_winner(player) or little_game.is_winner(opponent)
        self.assertTrue(result, "Found no winners!")
        pass

    def test_only_move(self):
        self.player1 = "Player1"
        self.player2 = "Player2"
        little_game = isolation.Board(self.player1, self.player2, width=1, height=1)

        Player_agent = game_agent.MinimaxPlayer()
        move = Player_agent.get_move(little_game, 10)
        self.assertEqual(move, (0,0), "Didn't return the best move")
        pass

    def test_loss_in_one(self):
        self.player1 = "Player1"
        self.player2 = "Player2"
        little_game = isolation.Board(self.player1, self.player2, width=3, height=2)
        Player_agent = game_agent.MinimaxPlayer()

        player = little_game.active_player
        opponent = little_game.inactive_player

        little_game.apply_move((0,0))
        move = Player_agent.get_move(little_game, 10)

        little_game.apply_move(move)

        self.assertTrue(little_game.is_winner(opponent), "Best move not working! choosen: {} against: (2,1)".format(move))
        ##################################################
        Player_agent = game_agent.AlphaBetaPlayer()

        player = little_game.active_player
        opponent = little_game.inactive_player

        little_game.apply_move((0,0))
        move = Player_agent.get_move(little_game, 10)

        little_game.apply_move(move)

        self.assertTrue(little_game.is_winner(opponent), "Best move not working! choosen: {} against: (2,1)".format(move))

        pass

    # (column, row) from 0 to n - 1 where n is the length of the size
    def test_correct_path_minimax(self):
        """
        " Simulate the path wich minimax could choose and check if it's a correct one
        """
        self.player1 = "Player1"
        self.player2 = "Player2"
        little_game = isolation.Board(self.player1, self.player2, width=3, height=3)
        Player_agent = game_agent.MinimaxPlayer()

        player = little_game.active_player
        opponent = little_game.inactive_player

        little_game.apply_move((0,0))
        little_game.apply_move((1,0))

        possible_paths = [[(1,2), (2,2), (2,0), (0,1)], [(2,1), (0,2)], [(2,1), (2,2), (0,2), (0,1)]]
        game_path = []

        while not (little_game.is_winner(player) or little_game.is_winner(opponent))    :
            move = Player_agent.get_move(little_game, 10)
            game_path += [move]
            little_game.apply_move(move)

        self.assertTrue(game_path in possible_paths, "Didn't choose a valid path, choosen: {}".format(game_path))
        ##############################################
        little_game = isolation.Board(self.player1, self.player2, width=3, height=3)
        Player_agent = game_agent.MinimaxPlayer()

        player = little_game.active_player
        opponent = little_game.inactive_player

        little_game.apply_move((0,0))
        little_game.apply_move((1,0))

        possible_paths = [[(1,2), (2,2), (2,0), (0,1)], [(2,1), (0,2)], [(2,1), (2,2), (0,2), (0,1)]]
        game_path = []

        while not (little_game.is_winner(player) or little_game.is_winner(opponent))    :
            move = Player_agent.get_move(little_game, 10)
            game_path += [move]
            little_game.apply_move(move)

        self.assertTrue(game_path in possible_paths, "Didn't choose a valid path, choosen: {}".format(game_path))
        pass

    def test_correct_path_alphabeta(self):
        """
        " Simulate the path wich minimax could choose and check if it's a correct one
        """
        self.player1 = "Player1"
        self.player2 = "Player2"
        little_game = isolation.Board(self.player1, self.player2, width=3, height=3)
        Player_agent = game_agent.AlphaBetaPlayer()

        player = little_game.active_player
        opponent = little_game.inactive_player

        little_game.apply_move((0,0))
        little_game.apply_move((1,0))

        possible_paths = [[(1,2), (2,2), (2,0), (0,1)], [(2,1), (0,2)], [(2,1), (2,2), (0,2), (0,1)]]
        game_path = []

        while not (little_game.is_winner(player) or little_game.is_winner(opponent))    :
            move = Player_agent.get_move(little_game, 10)
            game_path += [move]
            little_game.apply_move(move)

        self.assertTrue(game_path in possible_paths, "Didn't choose a valid path, choosen: {}".format(game_path))

        pass

if __name__ == '__main__':
    unittest.main()

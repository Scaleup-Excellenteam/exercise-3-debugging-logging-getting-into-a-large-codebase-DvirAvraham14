# test_piece.py

import pytest
from unittest.mock import Mock, patch
from chess_engine import game_state
from Piece import Knight, Pawn, King, Queen, Bishop, Rook
from enums import Player
import ai_engine


class TestKnight:
    @pytest.fixture
    def game(self):
        return game_state()

    @pytest.fixture
    def empty_board(self):
        game = game_state()
        game.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
        return game

    """
    Unit tests for Knight class methods
            Test: get_valid_peaceful_moves
            Test: get_valid_piece_takes
    """

    def test_knight_get_valid_peaceful_moves_center(self, game):
        knight = Knight('n', 4, 4, Player.PLAYER_1)
        with patch.object(game, 'get_piece', return_value=Player.EMPTY):
            moves = knight.get_valid_peaceful_moves(game)
            expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
            assert set(moves) == set(expected_moves)

    def test_knight_get_valid_peaceful_moves_corner(self, game):
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        game.get_piece = Mock(side_effect=
                              lambda r, c:
                              Player.EMPTY if ((r, c) != (0, 0) and (0 <= r < 8) and (0 <= c < 8)) else None)
        moves = knight.get_valid_peaceful_moves(game)
        expected_moves = [(1, 2), (2, 1)]
        assert set(moves) == set(expected_moves)

    def test_knight_get_valid_peaceful_moves_edge(self, game):
        knight = Knight('n', 4, 0, Player.PLAYER_1)
        game.get_piece = Mock(side_effect=
                              lambda r, c:
                              Player.EMPTY if ((r, c) != (0, 0) and (0 <= r < 8) and (0 <= c < 8)) else None)
        moves = knight.get_valid_peaceful_moves(game)
        expected_moves = [(2, 1), (3, 2), (5, 2), (6, 1)]
        assert set(moves) == set(expected_moves)

    def test_get_valid_piece_takes_center(self, game):
        knight = Knight('n', 4, 4, Player.PLAYER_1)
        moves = knight.get_valid_piece_takes(game)
        expected_moves = [(6, 3), (6, 5)]
        assert set(moves) == set(expected_moves)

    def test_get_valid_piece_takes_not_capture_is_own_pieces(self, game):
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        moves = knight.get_valid_piece_takes(game)
        expected_moves = []
        assert set(moves) == set(expected_moves)

    def test_knight_get_valid_piece_takes_capturing(self, empty_board):
        empty_board.board[2][1] = Knight('n', 2, 1, Player.PLAYER_2)
        knight = Knight('n', 0, 0, Player.PLAYER_1)
        empty_board.board[0][0] = knight
        moves = knight.get_valid_piece_takes(empty_board)
        expected_moves = [(2, 1)]
        assert set(moves) == set(expected_moves)

    """
    Integration tests for Knight class methods
            Test: get_valid_piece_moves
    """

    def test_get_valid_moves(self, game):
        """
        Test that get_valid_moves returns the expected moves for a Knight
        """
        # Set up a game state with a known board configuration
        game.board[3][3] = Knight('n', 3, 3, Player.PLAYER_1)
        # Mock the get_valid_piece_takes and get_valid_peaceful_moves methods
        with patch.object(Knight, 'get_valid_piece_takes') as mock_takes, \
                patch.object(Knight, 'get_valid_peaceful_moves') as mock_moves:
            # Set the return values for the mocks
            mock_takes.return_value = [(2, 1), (4, 1)]
            mock_moves.return_value = [(1, 2), (2, 5)]

            # Call get_valid_moves for the Knight
            valid_moves = game.get_valid_moves((3, 3))

            # Verify that the expected moves were returned
            expected_moves = [(1, 2), (2, 5), (2, 1), (4, 1)]
            assert set(valid_moves) == set(expected_moves)

    # Test for chess_ai evaluate_board
    def test_evaluate_board(self, empty_board):
        empty_board.board[3][3] = Knight("k", 3, 3, Player.PLAYER_1)  # white king
        empty_board.board[5][5] = Knight("q", 5, 5, Player.PLAYER_2)  # black queen
        chess_ai = ai_engine.chess_ai()
        print(empty_board)
        evaluation_score = chess_ai.evaluate_board(empty_board, Player.PLAYER_1)
        assert evaluation_score == -900  # white's king is threatened by black's queen (-900 points)

    # System test
    def test_fools_checkmate(self, game):
        """
        Test that the game correctly identifies a checkmate
        """
        # Moves for the Fools Mate
        game.move_piece((1, 2), (2, 2), False)
        game.move_piece((6, 3), (5, 3), False)
        game.move_piece((1, 1), (3, 1), False)
        game.move_piece((7, 4), (3, 0), False)
        result = game.checkmate_stalemate_checker()
        assert result == 0

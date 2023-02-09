"""Contains tests for the TicTacToe.py module.
    - test_returns_correct_game_name: Checks that the name of the game is returned as expected.
    - test_empty_board: Tests that empty board initializes as expected.
    - test_checkValidMove_correctly_evaluates_valid_moves: Tests that the checkValidMove function correctly identifies
        empty spaces as valid moves, and filled spaces as invalid moves.
    - test_updateBoard_updates_board_correctly: Tests that updateBoard function correctly assigns player icons to spaces.
    - test_checkBoard_correctly_identifies_all_endgame_scenarios: Tests that the checkBoard function correctly
        identifies win, draw, and GAME_IN_PROGRESS states.
    - test_bot_takes_wins: Tests that the bot will take wins when possible.
    - test_bot_blocks_wins: Tests that the bot will block opponent wins when possible.
    - test_resetGame: Tests that the resetGame function properly resets the game.
    - test_updatePlayerIcons_assigns_icons: Tests that the updatePlayerIcons function correctly assigns selected icons.
"""

import TicTacToe
import pytest
from string import printable as printable_chars


@pytest.fixture
def tic_tac_toe():
    """PyTest Fixture allows for easy initialization of class object in each test.

    :return: clean TicTacToe object to be used in each test.
    """
    return TicTacToe.TicTacTerminal()


def test_returns_correct_game_name(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Checks that the name of the game is returned as expected.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    assert tic_tac_toe.gameName() == "Tic-Tac-Toe"


def test_empty_board(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that empty board initializes as expected.

    :param tic_tac_toe: :param tic_tac_toe: the TicTacToe object to be used in the test
    :return:
    """
    assert tic_tac_toe.emptyBoard() == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]


def test_checkValidMove_correctly_evaluates_valid_moves(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the checkValidMove function correctly identifies empty spaces as valid moves,
    and filled spaces as invalid moves.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Initialize an empty board for the test
    tic_tac_toe.board = [
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS]
    ]

    # check that each space is a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is True

    # Initialize a full board of PLAYER_0 for the test
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0]
    ]

    # check that each space is not a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is False

    # Initialize a full board of PLAYER_1 for the test
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1]
    ]

    # check that each space is not a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is False


def test_updateBoard_updates_board_correctly(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that updateBoard function correctly assigns player icons to spaces.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Initialize an empty board for the test
    tic_tac_toe.board = [
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS]
    ]
    # Model board is manually updated in the test to make comparisons for expected results
    model_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    # Check each row and column
    for i in range(0, 3):
        for j in range(0, 3):
            # Update model board manually to check results
            model_board[i][j] = tic_tac_toe.PLAYER_0
            # Update using tested function
            tic_tac_toe.updateBoard(i, j, tic_tac_toe.PLAYER_0)
            assert tic_tac_toe.board == model_board


def test_checkBoard_correctly_identifies_all_endgame_scenarios(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the checkBoard function correctly identifies win, draw, and GAME_IN_PROGRESS states.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Win scenarios to be tested
    WIN_OPTIONS = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    # Test for each player icon
    game_states_to_check = (
        (tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0_WINNER),
        (tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1_WINNER)
    )
    # Test each icon in each win scenario
    for icon, expected_winner in game_states_to_check:
        for scenario in WIN_OPTIONS:
            tic_tac_toe.board = [
                [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
                [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
                [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS]
            ]
            for space in scenario:
                tic_tac_toe.board[space[0]][space[1]] = icon
            tic_tac_toe.checkBoard()
            assert tic_tac_toe.game_state == expected_winner

    # Test a draw game state
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_0],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1]
    ]
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.DRAW_GAME

    # Test a GAME_IN_PROGRESS state
    tic_tac_toe.board = tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.BLANK_POS, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_0],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1]
    ]
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.GAME_IN_PROGRESS


def test_bot_takes_wins(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the bot will take wins when possible.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Scenarios to be checked
    WIN_OPTIONS = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    # For each scenario, reset board and test
    for scenario in WIN_OPTIONS:
        tic_tac_toe.board = [
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS]
        ]
        # Set up a win scenario for the bot and let it move once
        for space in (scenario[0], scenario[1]):
            tic_tac_toe.board[space[0]][space[1]] = tic_tac_toe.PLAYER_1
        bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1)
        tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1)
        assert tic_tac_toe.board[scenario[2][0]][scenario[2][1]] == tic_tac_toe.PLAYER_1

    # Give the bot some more complex scenarios -- block opponent or win? (Should choose win)
    # Check a scenario involving rows
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.BLANK_POS]
    ]
    bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1)
    tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1)
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.PLAYER_1_WINNER

    # Check a scenario involving columns
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.BLANK_POS, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.BLANK_POS, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1]
    ]
    bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1)
    tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1)
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.PLAYER_1_WINNER


def test_bot_blocks_wins(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the bot will block opponent wins when possible.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Scenarios to be checked
    WIN_OPTIONS = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    # For each scenario, reset the board and test
    for scenario in WIN_OPTIONS:
        tic_tac_toe.board = [
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS],
            [tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS, tic_tac_toe.BLANK_POS]
        ]
        # Set up a win scenario for the opponent and let the bot move once
        for space in (scenario[0], scenario[1]):
            tic_tac_toe.board[space[0]][space[1]] = tic_tac_toe.PLAYER_0
        bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1)
        tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1)
        assert tic_tac_toe.board[scenario[2][0]][scenario[2][1]] == tic_tac_toe.PLAYER_1


def test_resetGame(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the resetGame function properly resets the game.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """

    # Initialize a filled board and game state
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1],
        [tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_1, tic_tac_toe.PLAYER_0],
        [tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_0, tic_tac_toe.PLAYER_1]
    ]
    tic_tac_toe.game_state = tic_tac_toe.PLAYER_0_WINNER

    # Run tested function
    tic_tac_toe.resetGame()

    # Test board and game state
    assert tic_tac_toe.emptyBoard() == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert tic_tac_toe.game_state == tic_tac_toe.GAME_IN_PROGRESS


def test_updatePlayerIcons_assigns_icons(tic_tac_toe: TicTacToe.TicTacTerminal):
    """Tests that the updatePlayerIcons function correctly assigns selected icons.
    Yup, we really be testing everything here.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """

    # Iterate through all printable characters, two at a time
    for i in range(0, len(printable_chars), 2):

        # Assign odd indexed characters to j, evens are assigned to i
        j = i + 1
        icon1 = printable_chars[i]
        icon2 = printable_chars[j]

        # Run the tested function and check result
        tic_tac_toe.updatePlayerIcons(icon1, icon2)
        assert tic_tac_toe.PLAYER_0_ICON == icon1
        assert tic_tac_toe.PLAYER_1_ICON == icon2


def test_bot_avoids_double_middle_trap(tic_tac_toe):
    # cases that can trap the bot into a loss,
    # in the format (move1, move2, move3, move_to_avoid)
    scenarios_to_check = [
        [(0, 1), (1, 1), (1, 0), (2, 2)],
        [(0, 1), (2, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 0)],
        [(0, 1), (2, 0), (1, 2), (1, 1)],
        [(2, 1), (1, 1), (1, 2), (0, 0)],
        [(2, 1), (0, 0), (1, 2), (1, 1)],
        [(2, 1), (1, 1), (1, 0), (0, 2)],
        [(2, 1), (0, 2), (1, 0), (1, 1)]
    ]
    # Run several times to account for randomness in bot decisions
    for _ in range(0, 10):
        for scenario in scenarios_to_check:
            # Initialize empty board
            tic_tac_toe.board = tic_tac_toe.emptyBoard()
            # simulate the scenario
            tic_tac_toe.updateBoard(scenario[0][0], scenario[0][1], tic_tac_toe.PLAYER_0)
            tic_tac_toe.updateBoard(scenario[1][0], scenario[1][1], tic_tac_toe.PLAYER_1)
            tic_tac_toe.updateBoard(scenario[2][0], scenario[2][1], tic_tac_toe.PLAYER_0)
            # let the bot move once
            move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1)
            # move should NOT be the center
            assert move != (1, 1)
            # move SHOULD be a corner (besides the trap corner, see next assert)
            assert (move[0] + move[1]) % 2 == 0
            tic_tac_toe.updateBoard(move[0], move[1], tic_tac_toe.PLAYER_1)
            # check that the bot successfully avoided the trap
            assert tic_tac_toe.board[scenario[3][0]][scenario[3][1]] != tic_tac_toe.PLAYER_1
            tic_tac_toe.move_history = []

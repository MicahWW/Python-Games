import TicTacToe
import pytest
from string import printable as printable_chars


@pytest.fixture
def tic_tac_toe():
    """PyTest Fixture allows for easy initialization of class object in each test.

    :return: clean TicTacToe object to be used in each test.
    """
    return TicTacToe.TicTacToe()


def test_returns_correct_game_name(tic_tac_toe):
    """Checks that the name of the game is returned as expected.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    assert tic_tac_toe.gameName() == "Tic-Tac-Toe"


def test_empty_board(tic_tac_toe):
    """Tests that empty board initializes as expected.

    :param tic_tac_toe: :param tic_tac_toe: the TicTacToe object to be used in the test
    :return:
    """
    assert tic_tac_toe.emptyBoard() == [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]


def test_checkValidMove_correctly_evaluates_valid_moves(tic_tac_toe):
    """Tests that the checkValidMove function correctly identifies empty spaces as valid moves,
    and filled spaces as invalid moves.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Initialize an empty board for the test
    tic_tac_toe.board = [
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON]
    ]

    # check that each space is a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is True

    # Initialize a full board of PLAYER_0_ICON for the test
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON],
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON],
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON]
    ]

    # check that each space is not a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is False

    # Initialize a full board of PLAYER_1_ICON for the test
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON],
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON],
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON]
    ]

    # check that each space is not a valid move
    for i in range(0, 3):
        for j in range(0, 3):
            assert tic_tac_toe.checkValidMove(i, j) is False


def test_updateBoard_updates_board_correctly(tic_tac_toe):
    """Tests that updateBoard function correctly assigns player icons to spaces.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Initialize an empty board for the test
    tic_tac_toe.board = [
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
        [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON]
    ]
    # Model board is manually updated in the test to make comparisons for expected results
    model_board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    # Define acceptable player icons
    icons_to_test = printable_chars
    # Check functionality for each possible icon
    for char in icons_to_test:
        # Assign icon to a player icon
        tic_tac_toe.PLAYER_0_ICON = char
        # Check each row and column
        for i in range(0, 3):
            for j in range(0, 3):
                # Update model board manually to check results
                model_board[i][j] = tic_tac_toe.PLAYER_0_ICON
                # Update using tested function
                tic_tac_toe.updateBoard(i, j, tic_tac_toe.PLAYER_0_ICON)
                assert tic_tac_toe.board == model_board


def test_checkBoard_correctly_identifies_all_endgame_scenarios(tic_tac_toe):
    """Tests that the checkBoard function correctly identifies win, draw, and no_winner states.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Win scenarios to be tested
    win_options = [
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
        (tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_WINNER),
        (tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_WINNER)
    )
    # Test each icon in each win scenario
    for icon, expected_winner in game_states_to_check:
        for scenario in win_options:
            tic_tac_toe.board = [
                [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
                [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
                [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON]
            ]
            for space in scenario:
                tic_tac_toe.board[space[0]][space[1]] = icon
            tic_tac_toe.checkBoard()
            assert tic_tac_toe.game_state == expected_winner

    # Test a draw game state
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_1_ICON],
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_0_ICON],
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_1_ICON]
    ]
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.DRAW_GAME

    # Test a no_winner state
    tic_tac_toe.board = tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.PLAYER_1_ICON],
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_0_ICON],
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_1_ICON]
    ]
    tic_tac_toe.checkBoard()
    assert tic_tac_toe.game_state == tic_tac_toe.NO_WINNER


def test_bot_takes_wins(tic_tac_toe):
    """Tests that the bot will take wins when possible.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Scenarios to be checked
    win_options = [
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
    for scenario in win_options:
        tic_tac_toe.board = [
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON]
        ]
        # Set up a win scenario for the bot and let it move once
        for space in (scenario[0], scenario[1]):
            tic_tac_toe.board[space[0]][space[1]] = tic_tac_toe.PLAYER_1_ICON
        bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1_ICON)
        tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1_ICON)
        assert tic_tac_toe.board[scenario[2][0]][scenario[2][1]] == tic_tac_toe.PLAYER_1_ICON


def test_bot_blocks_wins(tic_tac_toe):
    """Tests that the bot will block wins when possible.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """
    # Scenarios to be checked
    win_options = [
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
    for scenario in win_options:
        tic_tac_toe.board = [
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON],
            [tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON, tic_tac_toe.BLANK_POS_ICON]
        ]
        # Set up a win scenario for the opponent and let the bot move once
        for space in (scenario[0], scenario[1]):
            tic_tac_toe.board[space[0]][space[1]] = tic_tac_toe.PLAYER_0_ICON
        bot_move = tic_tac_toe.botMove(tic_tac_toe.PLAYER_1_ICON)
        tic_tac_toe.updateBoard(bot_move[0], bot_move[1], tic_tac_toe.PLAYER_1_ICON)
        assert tic_tac_toe.board[scenario[2][0]][scenario[2][1]] == tic_tac_toe.PLAYER_1_ICON


def test_resetGame(tic_tac_toe):
    """Tests that the resetGame function properly resets the game.

    :param tic_tac_toe: the TicTacToe object to be used in the test
    """

    # Initialize a filled board and game state
    tic_tac_toe.board = [
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_1_ICON],
        [tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_1_ICON, tic_tac_toe.PLAYER_0_ICON],
        [tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_0_ICON, tic_tac_toe.PLAYER_1_ICON]
    ]
    tic_tac_toe.game_state = tic_tac_toe.PLAYER_0_WINNER

    # Run tested function
    tic_tac_toe.resetGame()

    # Test board and game state
    assert tic_tac_toe.emptyBoard() == [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    assert tic_tac_toe.game_state == tic_tac_toe.NO_WINNER


def test_updatePlayerIcons_assigns_icons(tic_tac_toe):
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

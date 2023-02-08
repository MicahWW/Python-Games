import os
from typing import Tuple


class Checkers:
    """Contains the backend methods for running the Checkers game, to be inherited by platform-specific child classes.
    Built to work with terminal, API, GUI, and any other platforms (although at present, severely lacking in features).
    Highly plagiarized I mean "influenced" by the TicTacToe.TicTacToe class of this same project.

    Included methods:
     - __init__
     - gameName - returns the name of the game (namely, the name "Checkers")
     - newBoard - generates a new board with pieces in starting positions
     - checkValidMove - checks if a given move is valid; for valid moves, returns "True",
        and for invalid moves returns "False" and prints a message to the console.
     - updateBoard - assigns player icon (or blank position value) to a space and updates move history
     - jumpPiece - removes a jumped piece from the board
     - checkForWin - checks for wins by detecting when all of one player's pieces are gone
     - botMove - [FUTURE FEATURE TO BE CRAFTED AT A LATER DATE]
     - resetGame - Resets the board and game state, typically at the end of a game.
    """
    def __init__(self):
        # Board-space values
        self.BLANK_POS = 0x0
        self.PLAYER_1 = 0x1
        self.PLAYER_2 = 0x2
        self.UNREACHABLE_SPACE = 0x3
        # Game states
        self.GAME_IN_PROGRESS = 0x10
        self.PLAYER_1_WINNER = 0x20
        self.PLAYER_2_WINNER = 0x30
        self.STALEMATE = 0x40

        # Initialize beginning board and game state
        self.board = self.newBoard()
        self.game_state = self.GAME_IN_PROGRESS

        # Initialize move history
        self.move_history = []

    @staticmethod
    def gameName() -> str:
        """returns the name of the game, namely, "Checkers".
        :return: a string containing the name of the game
        """

        return "Checkers"

    def newBoard(self):
        """Creates a new board for the start of the game.

        :return: a new self.board object.
        """

        return [
            [self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2,
             self.UNREACHABLE_SPACE, self.PLAYER_2],
            [self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2,
             self.UNREACHABLE_SPACE],
            [self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2, self.UNREACHABLE_SPACE, self.PLAYER_2,
             self.UNREACHABLE_SPACE, self.PLAYER_2],
            [self.BLANK_POS, self.UNREACHABLE_SPACE, self.BLANK_POS, self.UNREACHABLE_SPACE, self.BLANK_POS, self.UNREACHABLE_SPACE,
             self.BLANK_POS, self.UNREACHABLE_SPACE],
            [self.UNREACHABLE_SPACE, self.BLANK_POS, self.UNREACHABLE_SPACE, self.BLANK_POS, self.UNREACHABLE_SPACE, self.BLANK_POS,
             self.UNREACHABLE_SPACE, self.BLANK_POS],
            [self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1,
             self.UNREACHABLE_SPACE],
            [self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1,
             self.UNREACHABLE_SPACE, self.PLAYER_1],
            [self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1, self.UNREACHABLE_SPACE, self.PLAYER_1,
             self.UNREACHABLE_SPACE]
        ]

    def checkValidMove(self, piece_col, piece_row, move_col, move_row, player_value) -> bool:
        """Determines if a given move is allowed, the returns a boolean (True for valid, False for invalid.)

        """

        # check that the selected spaces are in-bounds spaces
        if ((piece_col + piece_row) % 2 == 0) or ((move_col + move_row) % 2 == 0):
            print("That space is out of bounds!")
            return False
        # if the selected spaces are in bounds, proceed to other checks
        else:
            # Check that the space to move from is occupied by a piece the player owns
            if self.board[piece_row][piece_col] == player_value:
                # Check that the space to move to is empty
                if self.board[move_row][move_col] == self.BLANK_POS:
                    # Check that the space to move to is within 1 space (see elif for jumps)
                    if abs(piece_col - move_col) == 1 == abs(piece_row - move_row):
                        return True
                    # ... or that the space to move to is within jump distance
                    elif abs(piece_col - move_col) == 2 == abs(piece_row - move_row):
                        opponent_value = 0x3 - player_value
                        space_to_jump = (int((piece_col + move_col) / 2), int((piece_row + move_row) / 2))
                        # Check that there is an opponent piece to jump over
                        if self.board[space_to_jump[1]][space_to_jump[0]] == opponent_value:
                            self.jumpPiece(space_to_jump[0], space_to_jump[1])
                            return True
                    # Tried to move to a space too far away
                    else:
                        print("That space is too far away!")
                        return False
                # Tried to move to an already occupied space
                else:
                    print("There is already a piece there!")
                    return False
            # Tried to move from a space that does not have a piece the player owns
            else:
                print("You do not have a piece there!")
                return False

    def updateBoard(self, piece_col, piece_row, move_col, move_row, player_value) -> None:

        # Check that the passed player_value is a valid value
        if player_value in (self.PLAYER_1, self.PLAYER_2, self.BLANK_POS):
            # If value is valid, update the board and the move history and check for a finished game
            self.board[piece_row][piece_col] = self.BLANK_POS
            self.board[move_row][move_col] = player_value
            self.move_history.append((piece_col, piece_row, move_col, move_row, player_value))
            self.checkForWin()
        # If value is not valid, return an error
        else:
            err = (
                f"Tried to update the board with '{player_value}' but the only choices are "
                f"'{self.BLANK_POS}', '{self.PLAYER_1}', and '{self.PLAYER_2}'."
            )
            raise RuntimeError(err)

    def jumpPiece(self, jump_col, jump_row):
        # Remove a jumped piece from the board
        self.board[jump_row][jump_col] = self.BLANK_POS
        # What, you expected more?  It's a simple operation, man

    def checkForWin(self) -> None:
        # score_keeper keeps count of the remaining pieces
        score_keeper = {self.PLAYER_1: 0, self.PLAYER_2: 0}
        # count up the pieces
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] not in (self.BLANK_POS, self.UNREACHABLE_SPACE):
                    score_keeper[self.board[row][col]] += 1
        # if there are no player 1 pieces left, then player 2 has won
        if score_keeper[self.PLAYER_1] == 0:
            self.game_state = self.PLAYER_2_WINNER
        # if there are no player 2 pieces left, then player 1 has won
        elif score_keeper[self.PLAYER_2] == 0:
            self.game_state = self.PLAYER_1_WINNER
        # if there are pieces for both players on the board, the game continues (checkers has no draw/stalemate)
        else:
            self.game_state = self.GAME_IN_PROGRESS

    def botMove(self, bot_value: int) -> Tuple[int, int]:
        # bot forthcoming, need to write all the other backend logic first
        ...

    def resetGame(self) -> None:
        """Resets the board and game state, typically at the end of a game.
        Takes no arguments and makes no return.
        """

        self.board = self.newBoard()
        self.game_state = self.GAME_IN_PROGRESS


class CheckersTerminal(Checkers):

    def __init__(self):
        # Inherit from parent class, may they rest in piece (pun intended obviously)
        Checkers.__init__(self)

        # Colors for the board
        self.PLAYER_1_COLOR = "\033[1;34m"
        self.PLAYER_2_COLOR = "\033[1;32m"
        self.NEUTRAL_COLOR = "\033[0m"

        # How the players are displayed
        self.BLANK_POS_ICON = ' '
        self.UNREACHABLE_SPACE_ICON = ' '
        self.PLAYER_1_ICON = self.PLAYER_1_COLOR + '●' + self.NEUTRAL_COLOR
        self.PLAYER_2_ICON = self.PLAYER_2_COLOR + '▶' + self.NEUTRAL_COLOR

        # Default move structure (user-first single player)
        self.player_1_move = self.userMove
        self.player_2_move = self.botMove

    def promptUser(self) -> Tuple[int, int, int, int]:
        while True:
            # choose the piece to be moved
            choice = input("Select a piece: ")
            # choice should be in the format "g3" where "g" is column and "3" is row
            if len(choice) == 2:
                # convert to backend-friendly format
                piece_selection = self.processUserInput(choice)
                # choose where the piece will move to
                move_input = input("Where would you like to move this piece? ")
                # convert to backend-friendly format
                move_selection = self.processUserInput(move_input)
                # package the move into a tuple to be processed by other methods
                piece_col = piece_selection[0]
                piece_row = piece_selection[1]
                move_col = move_selection[0]
                move_row = move_selection[1]
                return piece_col, piece_row, move_col, move_row

            # also acceptable, full move in one input, ex "g3 h4"
            # where "g3" is the col,row of the piece to be moved
            # and "h4" is the space the piece will move to
            elif len(choice) == 5:
                # convert to backend-friendly format
                # "g3" and "h4" are sliced and passed as separate arguments to processUserInput method
                full_selection = self.processUserInput(choice[0:2], choice[3:5])
                # package move into tuple to be processed by other methods
                piece_col = full_selection[0]
                piece_row = full_selection[1]
                move_col = full_selection[2]
                move_row = full_selection[3]
                return piece_col, piece_row, move_col, move_row

    def processUserInput(self, selection, move=None):
        # column_dictionary translates user-input strings into int column values
        column_dictionary = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7
        }
        # input should be of format "g3" where "g" is col and "3" is row
        if len(selection) == 2 and move is None:
            if selection[0].isalpha() and selection[1].isnumeric():
                # convert the input into ints
                selection_col = column_dictionary[selection[0]]
                selection_row = 8 - int(selection[1])
                return selection_col, selection_row

        # also acceptable, full move in one input, ex "g3 h4"
        # where "g3" is the col,row of the piece to be moved
        # and "h4" is the space the piece will move to
        elif len(selection) == 2 and len(move) == 2:
            if selection[0].isalpha() and selection[1].isnumeric():
                if move[0].isalpha() and move[1].isnumeric():
                    # convert the input into ints
                    piece_col = column_dictionary[selection[0]]
                    piece_row = 8 - int(selection[1])
                    move_col = column_dictionary[move[0]]
                    move_row = 8 - int(move[1])
                    return piece_col, piece_row, move_col, move_row

        # if input is of neither accepted format, print error message for user
        self.invalidEntryMessage()

    @staticmethod
    def invalidEntryMessage():
        # clarify accepted input format for user
        print("Invalid entry\n"
              "Please enter a letter for column and a number for row, like 'a3'\n"
              "For help, type 'help'\n")

    def userMove(self, player_value: int) -> Tuple[int, int, int, int]:
        valid_move = False
        piece_col, piece_row, move_col, move_row = 0, 0, 0, 0

        # prompt user until a valid move is given
        while not valid_move:
            # unpack move tuple from promptUser
            piece_col, piece_row, move_col, move_row = self.promptUser()

            # checkValidMove returns True for valid moves, False for invalid moves
            valid_move = self.checkValidMove(piece_col, piece_row, move_col, move_row, player_value)

        # return the valid user move tuple
        return piece_col, piece_row, move_col, move_row

    def translateValueToIcon(self, board_position):
        # take the values in the backend board and translate them to user-readable icons
        if board_position == self.BLANK_POS:
            return self.BLANK_POS_ICON
        elif board_position == self.PLAYER_1:
            return self.PLAYER_1_ICON
        elif board_position == self.PLAYER_2:
            return self.PLAYER_2_ICON
        elif board_position == self.UNREACHABLE_SPACE:
            return self.UNREACHABLE_SPACE_ICON
        # all possible values should be accounted for at this point
        else:
            print("Something has gone wrong!")
            return "?"

    def displayBoard(self):
        result = "\n"
        # the board printout contains 19 rows, let's take them one at a time
        for i in range(0, 19):
            # "row" is the actual board row that is being worked on with any given iteration of the loop
            row = int((i - 2) / 2)
            # for odd i (except the very first and last), insert a row separator
            if i in range(3, 17, 2):
                result += " ╠════╬════╬════╬════╬════╬════╬════╬════╣\n"
            # before and after the board, insert column guides
            elif i == 0 or i == 18:
                result += "   a    b    c    d    e    f    g    h\n"
            # at the top of the board, print the top of the board
            elif i == 1:
                result += " ╔════╦════╦════╦════╦════╦════╦════╦════╗\n"
            # at the bottom of the board, print the bottom of the board
            elif i == 17:
                result += " ╚════╩════╩════╩════╩════╩════╩════╩════╝\n"
            # one row of spaces in the board and their vertical separators (using row variable)
            else:
                result += \
                    f"{ 8 - row}║  {self.translateValueToIcon(self.board[row][0])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][1])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][2])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][3])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][4])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][5])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][6])}" \
                    f" ║  {self.translateValueToIcon(self.board[row][7])} ║{8 - row}\n"
            # congratulations, you just finished a(nother) row!
            # If your i is not 18, back to the top and go again!
        # the entire board is assembled, print it!
        print(result)

    def terminalGame(self) -> None:
        # enable color on Windows terminals
        if os.name == "nt":
            os.system("color")

        # show the board to the user
        self.displayBoard()
        # Let's start the game!
        while True:
            print("First player's turn.")
            # prompt and accept the user's move
            piece_col, piece_row, move_col, move_row = self.userMove(self.PLAYER_1)
            # update the board with the user's move
            self.updateBoard(piece_col, piece_row, move_col, move_row, self.PLAYER_1)
            # print the board anew
            self.displayBoard()
            # check if the game is over (see updateBoard for game_state update)
            if self.game_state != self.GAME_IN_PROGRESS:
                print("Game over!")
                break

            # all the same but for the second player!
            print("Second player's turn.")
            piece_col, piece_row, move_col, move_row = self.userMove(self.PLAYER_2)
            self.updateBoard(piece_col, piece_row, move_col, move_row, self.PLAYER_2)
            self.displayBoard()
            if self.game_state != self.GAME_IN_PROGRESS:
                print("Game over!")
                break

        # at the end of the game, reset all and await instructions from main!
        self.resetGame()

# ... unless of course this IS main, in which case, just play the game once
if __name__ == "__main__":
    CheckersTerminal().terminalGame()
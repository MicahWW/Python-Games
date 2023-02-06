"""Contains the classes to run tic-tac-toe games.
	- TicTacToe: master class to be used for backend on any platform.
	- TicTacTerminal: child class of TicTacToe to be used for terminal-based games.
"""

import random
import os
from math import floor
from typing import Tuple, Optional, Union


##########################################################################################

class TicTacToe:
	"""Contains the backend methods for running the TicTacToe game, to be inherited by platform-specific child classes.
	Built to work with terminal, API, GUI, and any other platform.

	Included methods:
		- __init__(self)
		- gameName(self) - returns the name of the game (namely, the name "Tic-Tac-Toe")
		- emptyBoard(self) - generates an empty board
		- checkValidMove(self, row, col) - returns "True" if a move is valid
		- updateBoard(self, row, col, player_icon) - assigns player icon to a given space
		- checkBoard(self) - determines if the game has been won or drawn
		- botMove(self, player_icon) - brains of the bot for single-player mode
		- resetGame(self) - resets the board and game state, typically at the end of a game
	"""

	def __init__(self) -> None:
		"""Initializes the attributes for a TicTacToe game.

		Initializes TicTacToe instance with:
			- the player values, in hex codes
			- the available game states, in hex codes, including:
				- a game-in-progress state
				- one win state for each player
				- a draw state
			- an empty board (using emptyBoard method)
			- the beginning game state (game in progress)
			- the move history list (empty at start)
		"""

		# Player values
		self.BLANK_POS = 0x0
		self.PLAYER_0 = -0x1
		self.PLAYER_1 = 0x1
		# Game States
		self.GAME_IN_PROGRESS = 0x10
		self.PLAYER_0_WINNER = 0x20
		self.PLAYER_1_WINNER = 0x30
		self.DRAW_GAME = 0x40

		# Initialize empty board and state
		self.board = self.emptyBoard()
		self.game_state = self.GAME_IN_PROGRESS

		# Initialize move history
		self.move_history = []

	@staticmethod
	def gameName() -> str:
		"""returns the name of the game (namely, the name "Tic-Tac-Toe").
		:return: a string containing the name of the game.
		"""

		return "Tic-Tac-Toe"

	def emptyBoard(self) -> list:
		"""Creates an empty board for the start of a new game.

		:return: an empty self.board object.
		"""

		return [
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS],
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS],
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS]
		]

	def checkValidMove(self, row: int, col: int) -> bool:
		"""Determines if a given move is allowed, then returns a boolean (True for valid, False for invalid).

		:param row: the row of the space to be checked.
		:param col: the column of the space to be checked.
		:return: a boolean, True if the space is empty and the desired move is valid; False if the move is invalid.
		"""

		return self.board[row][col] == self.BLANK_POS

	def updateBoard(self, row: int, col: int, player_value: int) -> None:
		"""Updates the board and move history with new moves.

		Checks if given player_value is valid (including assigning a blank space),
		assigns player_value to position on board,
		appends move to move_history,
		and checks for wins.

		Makes no return.

		:param row: the row of the space to be updated.
		:param col: the column of the space to be updated.
		:param player_value: the icon to be put in the space (traditionally X, 0, or blank).
		"""

		# Check that the passed player_value is a valid value
		if player_value in (self.PLAYER_0, self.PLAYER_1, self.BLANK_POS):
			# If value is valid, update board and move history, then check for a win
			self.board[row][col] = player_value
			self.move_history.append((row, col))
			self.checkBoard()
		# If value is not valid, return an error
		else:
			err = (
				f"Tried to update the board with '{player_value}' but the only choices are "
				f"'{self.BLANK_POS}', '{self.PLAYER_0}', and '{self.PLAYER_1}'."
			)

			raise RuntimeError(err)

	def checkBoard(self) -> None:
		"""Checks the board for endgame scenarios; either a draw, or a win by either player.
		It then sets the game_state attribute accordingly.
		Takes no arguments and makes no return.
		"""

		# check for win in rows
		for row in range(0, 3):
			if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_0:
				self.game_state = self.PLAYER_0_WINNER
				return
			elif self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_1:
				self.game_state = self.PLAYER_1_WINNER
				return

		# check for win in columns
		for col in range(0, 3):
			if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_0:
				self.game_state = self.PLAYER_0_WINNER
				return
			elif self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_1:
				self.game_state = self.PLAYER_1_WINNER
				return

		# check for win in diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_0:
			self.game_state = self.PLAYER_0_WINNER
			return
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_0:
			self.game_state = self.PLAYER_0_WINNER
			return
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_1:
			self.game_state = self.PLAYER_1_WINNER
			return
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_1:
			self.game_state = self.PLAYER_1_WINNER
			return

		# check if the board is full
		for row in self.board:
			for col in row:
				if col == self.BLANK_POS:
					self.game_state = self.GAME_IN_PROGRESS
					return

		self.game_state = self.DRAW_GAME
		return

	def botMove(self, bot_icon: int) -> Tuple[int, int]:
		"""The brains of the most unbeatable bot this side of the singularity.
		Well, at least, it's pretty good now.  Still room for improvement.

		:param bot_icon: either self.PLAYER_0 or self.PLAYER_1, used by the bot to distinguish user from bot.
		:return: (row, col) as integers representing the row and column of bot's desired move.
		"""

		# Initialize valid_move as required by while loops
		valid_move = False
		# Initialize row and col, because it's the right thing to do
		row, col = 0, 0
		# Initialize not_bot_icon because who wants to read "self.PLAYER_1"
		# and all the logic that goes into figuring out if that's even the right icon to use?
		if bot_icon == self.PLAYER_0:
			not_bot_icon = self.PLAYER_1
		else:
			not_bot_icon = self.PLAYER_0

		# List of tuples containing the (row,col) of all possible win scenarios
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

		# check bot win scenarios by looping through WIN_OPTIONS list
		for option in WIN_OPTIONS:
			# Initialize score_keeper for reading the board for win scenarios
			score_keeper = {self.PLAYER_0: 0, self.PLAYER_1: 0, self.BLANK_POS: 0}
			# determine what is in each space and record with score_keeper
			# i is the individual space in any given win scenario, i[0] is row and i[1] is col
			for i in option:
				score_keeper[self.board[i[0]][i[1]]] += 1

			# If there are two bot icons set to win and a blank space available, take the blank space to win the game
			if score_keeper[bot_icon] == 2 and score_keeper[self.BLANK_POS] == 1:
				for i in option:
					if self.board[i[0]][i[1]] == self.BLANK_POS:
						row = i[0]
						col = i[1]
						return row, col
		# check for bot loss scenarios by looping through WIN_OPTIONS list
		for option in WIN_OPTIONS:
			# Initialize score_keeper for reading the board for win scenarios
			score_keeper = {self.PLAYER_0: 0, self.PLAYER_1: 0, self.BLANK_POS: 0}
			# determine what is in each space and record with score_keeper
			# i is the individual space in any given win scenario, i[0] is row and i[1] is col
			for i in option:
				score_keeper[self.board[i[0]][i[1]]] += 1
			# if there are two opponent icons set to win and a blank space available,
			# select the blank space to block the opponent from winning
			if score_keeper[not_bot_icon] == 2 and score_keeper[self.BLANK_POS] == 1:
				for i in option:
					if self.board[i[0]][i[1]] == self.BLANK_POS:
						row = i[0]
						col = i[1]
						return row, col

		# Check for middle-opener edge-case
		if bot_icon == self.PLAYER_1 and len(self.move_history) == 1:
			if self.board[1][1] == self.PLAYER_0:
				while not valid_move:
					row = random.choice((0, 2))
					col = random.choice((0, 2))
					valid_move = self.checkValidMove(row, col)
				return row, col

		# Check for edge-cases (that happen on turn 3)
		if bot_icon == self.PLAYER_1 and len(self.move_history) == 3:
			# Check for first edge-case: see board [[X, , ], [ ,X, ], [ , ,O]]
			# In this (or rotated) situation, bot should select a corner space
			if self.board[1][1] == self.PLAYER_0:
				# Check for scenario
				if (self.board[0][0] != self.BLANK_POS != self.board[2][2] != self.board[0][0]) or \
					(self.board[0][2] != self.BLANK_POS != self.board[2][0] != self.board[0][2]):
					# Select an open corner space
					while not valid_move:
						row = random.choice((0, 2))
						col = random.choice((0, 2))
						valid_move = self.checkValidMove(row, col)
					return row, col

			# Check for second edge-case: see board [[ ,X, ], [ ,O, ], [X, , ]]
			# In this scenario, bot loses if it selects (2, 1).  Avoid this (or rotated) scenarios.
			if self.board[1][1] == bot_icon:
				if self.board[0][1] != self.board[1][1] != self.board[2][1] != self.board[0][1]:
					while not valid_move:
						row = random.choice((0, 1, 2))
						col = random.choice((0, 1, 2))
						valid_move = self.checkValidMove(row, col)
						if (row, col) in ((0, 1), (2, 1)):
							valid_move = False
					return row, col
				elif self.board[1][0] != self.board[1][1] != self.board[1][2] != self.board[1][0]:
					while not valid_move:
						row = random.choice((0, 1, 2))
						col = random.choice((0, 1, 2))
						valid_move = self.checkValidMove(row, col)
						if (row, col) in ((1, 0), (1, 2)):
							valid_move = False
					return row, col

		# If the bot escapes the win-checker loop and edge-cases, select a space using criteria
		# Explanation of criteria: imagine a tic-tac-toe board colored like checkerboard.
		# If human player plays on white space, bot tries to play black space, or vice versa.
		# This is implemented using an odd/even scheme of the board positions.
		last_opponent_move = self.move_history[-1]
		# escape_counter prevents infinite loops if the above criteria cannot be followed
		# (likely due to a nearly-filled board)
		escape_counter = 9
		while not valid_move:
			# Prefer the center space on 2nd move if available
			if len(self.move_history) == 1 and self.board[1][1] == self.BLANK_POS:
				row, col = (1, 1)
			else:
				row = random.choice((0, 1, 2))
				# check if opponent moved to "even" or "odd" space and counter appropriately
				if (last_opponent_move[0] + last_opponent_move[1]) % 2 == 0:
					if row in (0, 2):
						col = 1
					else:
						col = random.choice((0, 2))
				else:
					if row == 1:
						col = 1
					else:
						col = random.choice((0, 2))
			valid_move = self.checkValidMove(row, col)

			# It is possible that there will be only evens or only odds available;
			# if that seems to be the case, escape the odd/even loop and take any available space.
			escape_counter -= 1
			if escape_counter <= 0:
				row = random.choice((0, 1, 2))
				col = random.choice((0, 1, 2))
				valid_move = self.checkValidMove(row, col)

		return row, col

	def resetGame(self) -> None:
		"""Resets the board and game state, typically at the end of a game.
		Takes no arguments and makes no return.
		"""

		self.board = self.emptyBoard()
		self.game_state = self.GAME_IN_PROGRESS


class TicTacTerminal(TicTacToe):
	"""Contains methods specialized for playing tic-tac-toe games in the terminal.  Inherits from TicTacToe class.

	Included methods:
		- __init__(self)
		- updatePlayerIcons(self, player_0_icon, player_1_icon): Assigns custom player icons.
		- advancedGameSettings(self, setting_to_change=None): Allows user to change additional game settings.
		- gameSettingsPrompt(self): Prints messages to allow the user to select number of players and choose icons.
		- terminalGame(self): Starts a TicTacToe game in the terminal and calls supporting methods.
		- displayBoard(self): Prints the board for the user to see.
		- displayResult(self): Checks the game_state and displays how the game ended.
		- userMove(self, player_icon): Processes everything that is needed for a user to make a move.
		- promptUser(self): Connects userMove and userInputHandler to prompt for and accept user input.
		- userInputHandler(self, prompt, exclusions=None): Allows user to select special options from any input point;
			otherwise behaves like built-in input function.
	"""

	def __init__(self) -> None:
		"""Initializes additional attributes for a TicTacToe game in the terminal.

		Initializes the TicTacTerminal instance with:
			- inherited attributes from TicTacToe parent class
			- colors for the board
			- default player icons
			- default move structure (user-first single player, likely overwritten in gameSettingsPrompt)
		"""

		TicTacToe.__init__(self)

		# Colors for the board
		self.blank_pos_color = "\033[1;32m"
		self.exit_color_code = "\033[0m"

		# How the players are displayed
		self.PLAYER_0_ICON = 'X'
		self.PLAYER_1_ICON = 'O'

		# Default move structure (user-first single player)
		self.player_0_move = self.userMove
		self.player_1_move = self.botMove

	def updatePlayerIcons(self, player_0_icon: str, player_1_icon: str) -> None:
		"""Assigns custom player icons to self.PLAYER_0_ICON and self.PLAYER_1_ICON.
		Makes no return.

		:param player_0_icon: The character to be assigned as the player 0 icon.
		:param player_1_icon: The character to be assigned as the player 1 icon.
		"""
		self.PLAYER_0_ICON = player_0_icon
		self.PLAYER_1_ICON = player_1_icon

	def advancedGameSettings(self, setting_to_change: Optional[str] = None) -> None:
		"""Allows user to change additional game settings.

		Allows for changing:
			- player icons
			- actually that's it for now
			- it just seemed like a good idea to start this format for later when there are more options

		Makes no return.

		:param setting_to_change: specifies what the user would like to change.
		"""
		if setting_to_change is None:
			setting_to_change = self.userInputHandler('What setting do you want to change? ', 'settings')

		match setting_to_change:
			case 'change icons':
				print('Both player icons must only be 1 character long.')
				player0 = 'too long'
				while len(player0) != 1:

					player0 = self.userInputHandler('What do you want first move icon to be? (Traditionally X): ', 'settings')
					if len(player0) != 1:
						print("Please enter a single character for the player icon")

				player1 = 'too long'
				while len(player1) != 1:
					player1 = self.userInputHandler('What do you want second move icon to be? (Traditionally O): ', 'settings')
					if len(player0) != 1:
						print("Please enter a single character for the player icon")

				self.updatePlayerIcons(player0, player1)
			case _:
				raise Exception(f"Was given {setting_to_change} but that doesn't exist")

	def gameSettingsPrompt(self) -> None:
		"""Prints messages to allow the user to select number of players and choose icons.
		Takes no arguments and makes no return.
		"""

		# Prompts for how many human players there will be
		num_players = 0
		while num_players != 1 and num_players != 2:
			num_players = self.userInputHandler("Enter the number of players (1 or 2): ")
			if num_players.isnumeric():
				num_players = int(num_players)
			elif num_players == 'change icons':
				self.advancedGameSettings(num_players)

		# if user selected single player
		if num_players == 1:
			# choose the player icon
			player_choice = self.BLANK_POS
			while player_choice != self.PLAYER_0_ICON and player_choice != self.PLAYER_1_ICON:
				player_choice = self.userInputHandler(
					f"{self.PLAYER_0_ICON}s plays first, do you want to be {self.PLAYER_0_ICON} or {self.PLAYER_1_ICON}? "
				)
				if player_choice != self.PLAYER_0_ICON and player_choice != self.PLAYER_1_ICON:
					print("That is not a valid option, make sure to match the letter's upper/lower case.")

			# set the players based off the user's choice
			if player_choice == self.PLAYER_0_ICON:
				self.player_0_move = self.userMove
				self.player_1_move = self.botMove
			else:
				self.player_0_move = self.botMove
				self.player_1_move = self.userMove
		# multiplayer
		else:
			print(f"{self.PLAYER_0_ICON}s plays first, decide who will be the first player.")
			self.player_0_move = self.userMove
			self.player_1_move = self.userMove

	def terminalGame(self) -> None:
		"""Starts a TicTacToe game in the terminal and calls supporting methods.
		Takes no arguments and makes no return.
		"""

		# Enable color on Windows terminals
		if os.name == "nt":
			os.system("color")

		# Set up the game
		self.gameSettingsPrompt()

		print("If you wish to stop playing the game enter 'exit'.")
		# Start of game
		self.displayBoard()
		while True:
			print("First player's turn.")
			row, col = self.player_0_move(self.PLAYER_0)
			if row == -1 and col == -1: break  # noqa: E701
			self.updateBoard(row, col, self.PLAYER_0)
			self.displayBoard()
			if self.game_state != self.GAME_IN_PROGRESS: break  # noqa: E701

			print("Second player's turn.")
			row, col = self.player_1_move(self.PLAYER_1)
			if row == -1 and col == -1: break  # noqa: E701
			self.updateBoard(row, col, self.PLAYER_1)
			self.displayBoard()
			if self.game_state != self.GAME_IN_PROGRESS: break  # noqa: E701

		# End of game; display winner/draw and reset
		self.displayResult()
		self.resetGame()

	def displayBoard(self) -> None:
		"""Prints the board for the user to see.

		Takes no arguments and makes no return.
		rather, calls the self.board object directly and prints directly to console.
		"""

		# Ensure margin with text by beginning with newline
		result = "\n"
		for i in range(0, 9):
			row = floor(i / 3)
			col = i % 3
			# First column, requires tab indent to create margin with edge of window
			if i in (0, 3, 6):
				if self.board[row][col] != self.BLANK_POS:
					result += f"\t {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON} ║"
				else:
					result += f"\t{self.blank_pos_color} {i + 1} {self.exit_color_code}║"
			# Second column, requires only a space on each side of icon plus right-side seperator
			elif i in (1, 4, 7):
				if self.board[row][col] != self.BLANK_POS:
					result += f" {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON} ║"
				else:
					result += f"{self.blank_pos_color} {i + 1} {self.exit_color_code}║"
			# Third column, requires vertical seperator (only on 1st and 2nd rows)
			elif i in (2, 5, 8):
				if self.board[row][col] != self.BLANK_POS:
					result += f" {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON}\n"
				else:
					result += f"{self.blank_pos_color} {i + 1} {self.exit_color_code}\n"
				if i in (2, 5):
					result += "\t═══╬═══╬═══\n"

		print(result)

	def displayResult(self) -> None:
		"""Checks the game_state and displays how the game ended.
		Takes no arguments and makes no return.
		"""

		if self.game_state == self.PLAYER_0_WINNER:
			print(f"{self.PLAYER_0_ICON} won the game!")
		elif self.game_state == self.PLAYER_1_WINNER:
			print(f"{self.PLAYER_1_ICON} won the game!")
		elif self.game_state == self.DRAW_GAME:
			print("The game ended in a draw")
		else:
			# for no winner
			pass

	def userMove(self, player_icon: Optional[int]) -> Tuple[int, int]:
		"""Processes everything that is needed for a user to make a move,
		including checking if input was valid (through promptUser, checkValidMove, etc.)

		:param player_icon: The player_icon is not used in userMove but is necessary to avoid bugs with botMove.
					See how player_icon argument is used in the botMove method,
					and how both of these methods are used in the terminalGame method for details.
		"""

		# Initialize valid_move as required by while loop
		valid_move = False
		# Initialize row and col, because it's the right thing to do
		row, col = 0, 0

		while not valid_move:
			# Allow user to select desired move
			row, col = self.promptUser()

			# Check for special inputs
			# row == -1 and col == -1 ends game immediately
			if row != -1 and col != -1:
				valid_move = self.checkValidMove(row, col)
				if not valid_move:
					print("That space is already taken")
			else:
				# return (-1, -1) to end game
				return row, col

		return row, col

	def promptUser(self) -> Tuple[int, int]:
		"""Connects userMove and userInputHandler to prompt for and accept user input.

		Requests user input for desired move on user's turn (via userInputHandler),
		validates that input is a single numeric character,
		converts 9-board format input to 3x3-board format,
		and then returns selected space to caller (usually userMove method).

		:return: (row, col) as the row and column of the space selected by the user for their move.
		"""

		while True:
			choice = self.userInputHandler("Where do you want to play? ")
			# validate: is single numeric character
			if len(choice) == 1 and choice.isnumeric():
				# convert from 1-9 digits as shown to user (see displayBoard)
				# to zero-indexed 3x3 format used by the rest of the program
				choice = int(choice) - 1
				row = floor(choice / 3)
				col = choice % 3

				return row, col
			# if user inputs "exit", return a special tuple to end the game
			elif choice == 'exit':
				return -1, -1

	def userInputHandler(self, prompt: str, exclusions: Union[list, str] = None) -> str:
		"""Allows user to select special options from any input point; otherwise behaves like built-in input function.

		:param prompt: string for the user to see, same as with built-in input(prompt) function
		:param exclusions: options the user is not allowed to select
		:return: user input as a string (in special cases does not return but rather runs a callable)
		"""
		# Special options available to the user
		options = {'settings': self.advancedGameSettings}
		while True:
			# Ensure exclusions is of type List
			if exclusions is None:
				exclusions = []
			elif isinstance(exclusions, list):
				pass
			elif isinstance(exclusions, str):
				exclusions = [exclusions]
			else:
				raise Exception(f"Variable exclusions can only be of type list or str, it is {type(exclusions)}")

			# prompt user for input
			selection = input(prompt)
			if selection not in exclusions:
				# check if input is a special option
				result = options.get(selection, 'pass')
				# if special option, run related callable (ex self.advancedGameSettings)
				if result != 'pass':
					result()
				# if not special case, return input as string
				else:
					return selection
			# user selects a blocked option (ex "settings" from within settings)
			else:
				print('You can not do that right now.')


if __name__ == "__main__":
	TicTacTerminal().terminalGame()

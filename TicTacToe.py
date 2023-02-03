import random
import os
from math import floor


##########################################################################################

class TicTacToe:
	"""Contains the objects and functions for running the TicTacToe game, to be called from main.py.

	Included functions:
		- __init__(self)
		- gameName(self) - returns the name of the game (namely, the name "Tic-Tac-Toe")
		- emptyBoard(self) - generates an empty board
		- checkValidMove(self, row, col) - returns "True" if a move is valid
		- updateBoard(self, row, col, player_icon) - assigns player icon to a given space
		- checkBoard(self) - determines if the game has been won or drawn
		- startTerminalGame(self) - outputs prompts and info to user and calls game functions
		- displayBoard(self) - prints the board to the console for the user to see
		- displayResult(self, game_state) - prints a win or draw message
		- userMove(self, player_icon) - takes user input to update the board
		- promptUser() - asks for and processes user input
		- botMove(self, player_icon) - brains of the bot for single-player mode
	"""

	def __init__(self):
		"""
		Initializes TicTacToe object with
			- player icons (traditionally X and O)
			- game states (a continue/no-winner state, one win state for each player, and a draw state)
			- and an empty board.
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
	def gameName():
		"""returns the name of the game (namely, the name "Tic-Tac-Toe").
		:return: a string containing the name of the game.
		"""

		return "Tic-Tac-Toe"

	def emptyBoard(self):
		"""Creates an empty board for the start of a new game.

		:return: an empty self.board object.
		"""

		return [
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS],
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS],
			[self.BLANK_POS, self.BLANK_POS, self.BLANK_POS]
		]

	def checkValidMove(self, row, col):
		"""Determines if a given move is allowed, then returns a boolean (True for valid moves, False for invalid moves).

		:param row: the row of the space to be checked.
		:param col: the column of the space to be checked.
		:return: a boolean, True if the space is empty and the desired move is valid; False if the move is invalid.
		"""

		return self.board[row][col] == self.BLANK_POS

	def updateBoard(self, row, col, player_values):
		"""Updates the board by assigning a player_icon to a given space, before doing so checks if a valid icon
		Does not return anything; assigns directly to the self.board object.

		:param row: the row of the space to be updated.
		:param col: the column of the space to be updated.
		:param player_values: the icon to be put in the space (traditionally X or O).
		"""

		if player_values in (self.PLAYER_0, self.PLAYER_1, self.BLANK_POS):
			self.board[row][col] = player_values
			self.move_history.append((row, col))
			self.checkBoard()
		else:
			err = (
				f"Tried to update the board with '{player_values}' but the only choices are "
				f"'{self.BLANK_POS}', '{self.PLAYER_0}', and '{self.PLAYER_1}'."
			)

			raise RuntimeError(err)

	def checkBoard(self):
		"""Checks the board for endgame scenarios, either a draw or a win by either player.
		It then sets the game_state attribute accordingly.
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

	def botMove(self, bot_icon):
		"""The brains of the most unbeatable bot this side of the singularity.

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

		# check win scenarios by looping through win_options list
		for option in win_options:
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
		for option in win_options:
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

		# Initialize turn counter
		turn_counter = 9
		for i in range(0, 3):
			for j in range(0, 3):
				if self.board[i][j] == self.BLANK_POS:
					turn_counter -= 1

		# Check for middle-opener edge-case
		if bot_icon == self.PLAYER_1 and turn_counter == 1:
			if self.board[1][1] == self.PLAYER_0:
				while not valid_move:
					row = random.choice((0, 2))
					col = random.choice((0, 2))
					valid_move = self.checkValidMove(row, col)
				return row, col

		# Check for edge-cases (that happen on turn 3)
		if bot_icon == self.PLAYER_1 and turn_counter == 3:
			# Check for first edge-case: see board [[X, , ], [ ,X, ], [ , ,O]]
			# In this (or rotated) situation, bot should select a corner space
			if self.board[1][1] == self.PLAYER_0:
				# Check for scenario
				if ((self.board[0][0] != self.BLANK_POS !=
					self.board[2][2] != self.board[0][0]) or
						(self.board[0][2] != self.BLANK_POS !=
						self.board[2][0] != self.board[0][2])):
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
		while not valid_move:
			if turn_counter == 1 and self.board[1][1] == self.BLANK_POS:
				row, col = (1, 1)
			else:
				row = random.choice((0, 1, 2))
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

		return row, col

	def resetGame(self):
		"""Takes the necessary game attributes and resets them to their beginning state
		Does not take in anything or return anything
		"""

		self.board = self.emptyBoard()
		self.game_state = self.GAME_IN_PROGRESS


class TicTacTerminal(TicTacToe):
	def __init__(self):
		TicTacToe.__init__(self)
		self.blank_pos_color = "\033[1;32m"
		self.exit_color_code = "\033[0m"

		# How the players are displayed
		self.PLAYER_0_ICON = 'X'
		self.PLAYER_1_ICON = 'O'

	def updatePlayerIcons(self, player_0_icon, player_1_icon):
		self.PLAYER_0_ICON = player_0_icon
		self.PLAYER_1_ICON = player_1_icon

	def advancedGameSettings(self, setting_to_change):
		match setting_to_change:
			case 'change icons':
				print('Both player icons must only be 1 character long.')
				player0 = 'too long'
				while len(player0) != 1:
					player0 = input('What do you want first move icon to be? (Traditionally X): ')
					if len(player0) != 1:
						print("Please enter a single character for the player icon")

				player1 = 'too long'
				while len(player1) != 1:
					player1 = input('What do you want second move icon to be? (Traditionally O): ')
					if len(player0) != 1:
						print("Please enter a single character for the player icon")

				self.updatePlayerIcons(player0, player1)

	def gameSettingsPrompt(self):
		"""Prints messages to allow the user to select number of players then choose their icon
		Takes no inputs

		:returns: a tuple of the functions to process the 0 and 1 player moves
		"""

		# Prompts for how many human players there will be
		num_players = 0
		while num_players != 1 and num_players != 2:
			num_players = input("Enter the number of players (1 or 2): ")
			if num_players.isnumeric():
				num_players = int(num_players)
			elif num_players == 'change icons':
				self.advancedGameSettings(num_players)

		# if user selected single player
		if num_players == 1:
			# choose the player icon
			player_choice = self.BLANK_POS
			while player_choice != self.PLAYER_0_ICON and player_choice != self.PLAYER_1_ICON:
				player_choice = input(
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

	def terminalGame(self):
		"""Starts a TicTacToe game in the terminal and calls supporting functions.
		Takes no inputs and makes no return.
		"""

		if os.name == "nt":
			os.system("color")

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

		self.displayResult()
		self.resetGame()

	def displayBoard(self):
		"""Prints the board for the user to see.

		Takes no arguments and gives no return;
		rather, calls the self.board object directly and prints directly to console.
		"""

		result = "\n"
		for i in range(0, 9):
			row = floor(i / 3)
			col = i % 3
			if i in (0, 3, 6):
				if self.board[row][col] != self.BLANK_POS:
					result += f"\t {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON} ║"
				else:
					result += f"\t{self.blank_pos_color} {i + 1} {self.exit_color_code}║"
			elif i in (1, 4, 7):
				if self.board[row][col] != self.BLANK_POS:
					result += f" {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON} ║"
				else:
					result += f"{self.blank_pos_color} {i + 1} {self.exit_color_code}║"

			elif i in (2, 5, 8):
				if self.board[row][col] != self.BLANK_POS:
					result += f" {self.PLAYER_0_ICON if self.board[row][col] == self.PLAYER_0 else self.PLAYER_1_ICON}\n"
				else:
					result += f"{self.blank_pos_color} {i + 1} {self.exit_color_code}\n"
				if i in (2, 5):
					result += "\t═══╬═══╬═══\n"

		print(result)

	def displayResult(self):
		"""Checks the game_state and displays how the game ended.
		It takes in nothing and returns nothing
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

	def userMove(self, player_icon):
		"""Processes everything that is needed for a user to make a move,
		including checking if input was valid (through promptUser(), spot is free to move in, etc.)

		:param player_icon: The player_icon is not used in userMove but is necessary to avoid bugs with botMove.
					See how player_icon argument is used in botMove(self, player_icon),
					and how both of these functions are used in startTerminalGame(self) for details.
		"""

		valid_move = False
		row, col = 0, 0

		while not valid_move:
			row, col = self.promptUser()
			if row != -1 and col != -1:
				valid_move = self.checkValidMove(row, col)
				if not valid_move:
					print("That space is already taken")
			else:
				return row, col

		return row, col

	@staticmethod
	def promptUser():
		"""Requests user input for desired move on user's turn, validates, and then returns selected space.

		:return: (row, col) as the row and column of the space selected by the user for their move.
		"""

		while True:
			choice = input("Where do you want to play? ")
			if len(choice) == 1 and choice.isnumeric():
				choice = int(choice) - 1
				row = floor(choice / 3)
				col = choice % 3

				return row, col
			elif choice == 'exit':
				return -1, -1


if __name__ == "__main__":
	TicTacTerminal().terminalGame()

import random
from datetime import datetime
from math import floor
import os

if os.name == "nt":
	os.system("color")

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
			- a random datetime seed
			- player icons (traditionally X and O)
			- game states (a continue/no-winner state, one win state for each player, and a draw state)
			- and an empty board.
		"""

		random.seed(datetime.now().strftime("%Y%m%d%H%M%S"))

		# Player Icons
		self.BLANK_POS_ICON = " "
		self.PLAYER_0_ICON = "X"
		self.PLAYER_1_ICON = "O"
		# Game States
		self.NO_WINNER = 0
		self.PLAYER_0_WINNER = 1
		self.PLAYER_1_WINNER = 2
		self.DRAW_GAME = 3

		# Initialize empty board and state
		self.board = self.emptyBoard()
		self.game_state = self.NO_WINNER

	@staticmethod
	def gameName():
		"""returns the name of the game (namely, the name "Tic-Tac-Toe").
		:return: a string containing the name of the game.
		"""

		return "Tic-Tac-Toe"

	##########################################################################################
	# behind the scenes functions

	def emptyBoard(self):
		"""Creates an empty board for the start of a new game.

		:return: an empty self.board object.
		"""

		return [
			[self.BLANK_POS_ICON, self.BLANK_POS_ICON, self.BLANK_POS_ICON],
			[self.BLANK_POS_ICON, self.BLANK_POS_ICON, self.BLANK_POS_ICON],
			[self.BLANK_POS_ICON, self.BLANK_POS_ICON, self.BLANK_POS_ICON]
			]

	def checkValidMove(self, row, col):
		"""Determines if a given move is allowed, then returns a boolean (True for valid moves, False for invalid moves).

		:param row: the row of the space to be checked.
		:param col: the column of the space to be checked.
		:return: a boolean, True if the space is empty and the desired move is valid; False if the move is invalid.
		"""

		return self.board[row][col] == self.BLANK_POS_ICON

	def updateBoard(self, row, col, player_icon):
		"""Updates the board by assigning a player_icon to a given space, before doing so checks if a valid icon
		Does not return anything; assigns directly to the self.board object.

		:param row: the row of the space to be updated.
		:param col: the column of the space to be updated.
		:param player_icon: the icon to be put in the space (traditionally X or O).
		"""

		if player_icon in (self.BLANK_POS_ICON, self.PLAYER_0_ICON, self.PLAYER_1_ICON):
			self.board[row][col] = player_icon
			self.checkBoard()
		else:
			err = f"Tried to update the board with '{player_icon}' but the only choices are '{self.BLANK_POS_ICON}', '{self.PLAYER_0_ICON}', and '{self.PLAYER_1_ICON}'."
			raise RuntimeError(err)

	def checkBoard(self):
		"""Checks the board for endgame scenarios, either a draw or a win by either player.
		It then sets the game_state attribute accordingly
		"""

		# check for win in rows
		for row in range(0, 3):
			if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_0_ICON:
				self.game_state = self.PLAYER_0_WINNER
				return
			elif self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_1_ICON:
				self.game_state = self.PLAYER_1_WINNER
				return

		# check for win in columns
		for col in range(0, 3):
			if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_0_ICON:
				self.game_state = self.PLAYER_0_WINNER
				return
			elif self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_1_ICON:
				self.game_state = self.PLAYER_1_WINNER
				return

		# check for win in diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_0_ICON:
			self.game_state = self.PLAYER_0_WINNER
			return
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_0_ICON:
			self.game_state = self.PLAYER_0_WINNER
			return
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_1_ICON:
			self.game_state = self.PLAYER_1_WINNER
			return
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_1_ICON:
			self.game_state = self.PLAYER_1_WINNER
			return

		# check if the board is full
		for row in self.board:
			for col in row:
				if col == self.BLANK_POS_ICON:
					self.game_state = self.NO_WINNER
					return

		self.game_state = self.DRAW_GAME
		return

	def botMove(self, player_icon):
		"""The brains of the most unbeatable bot this side of the singularity.
		Okay probably not, but it should at least block easy wins.

		:param player_icon: either self.PLAYER_0_ICON or self.PLAYER_1_ICON, used by the bot to distinguish user from bot.
		:return: (row, col) as integers representing the row and column of bot's desired move.
		"""

		# Initialize valid_move as required by the while loop
		valid_move = False
		# Initialize row and col, because it's the right thing to do
		row, col = 0, 0
		# Initialize not_bot_icon because who wants to read "self.PLAYER_1_ICON" and all the logic that goes into figuring out if that's even the right icon to use?
		if player_icon == self.PLAYER_0_ICON:
			not_bot_icon = self.PLAYER_1_ICON
		else:
			not_bot_icon = self.PLAYER_0_ICON
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
			score_keeper = {self.PLAYER_0_ICON: 0, self.PLAYER_1_ICON: 0, self.BLANK_POS_ICON: 0}
			# determine what is in each space and record with score_keeper
			# i is the individual space in any given win scenario, i[0] is row and i[1] is col
			for i in option:
				score_keeper[self.board[i[0]][i[1]]] += 1

			# If there are two bot icons set to win and a blank space available, take the blank space to win the game
			if score_keeper[player_icon] == 2 and score_keeper[self.BLANK_POS_ICON] == 1:
				for i in option:
					if self.board[i[0]][i[1]] == self.BLANK_POS_ICON:
						row = i[0]
						col = i[1]
						return row, col
			# if there are two opponent icons set to win and a blank space available, select the blank space to block the opponent from winning
			if score_keeper[not_bot_icon] == 2 and score_keeper[self.BLANK_POS_ICON] == 1:
				for i in option:
					if self.board[i[0]][i[1]] == self.BLANK_POS_ICON:
						row = i[0]
						col = i[1]
						return row, col

		# If the bot escapes the win-checker loop and finds no imminent win scenarios, select a random space
		while not valid_move:
			row = random.choice([0, 1, 2])
			col = random.choice([0, 1, 2])
			valid_move = self.checkValidMove(row, col)

		return row, col

	def resetGame(self):
		"""Takes the necessary game attributes and resets them to their begnining state
		Does not take in anything or returns anything
		"""

		self.board = self.emptyBoard()
		self.game_state = self.NO_WINNER

	# behind the scenes functions
	##########################################################################################
	# terminal functions

	def gameSettingsPrompt(self):
		"""Prints messages to allow the user to select number of players then choice which icon
		Takes no inputs
		:returns: a tuple of the functions to call to process the 0 and 1 player moves
		"""

		num_players = 0
		while num_players != 1 and num_players != 2:
			num_players = input("Enter the number of players (1 or 2): ")
			if num_players.isnumeric():
				num_players = int(num_players)
		
		# single player
		if num_players == 1:
			# choose the player icon
			player_choice = self.BLANK_POS_ICON
			while player_choice != self.PLAYER_0_ICON and player_choice != self.PLAYER_1_ICON:
				player_choice = input(f"{self.PLAYER_0_ICON}s plays first, do you want to be {self.PLAYER_0_ICON} or {self.PLAYER_1_ICON}? ")
				if player_choice != self.PLAYER_0_ICON and player_choice != self.PLAYER_1_ICON:
					print("That is not a valid option, make sure to match the letter's upper/lower case.")

			# set the players based off the user's choice
			if player_choice == self.PLAYER_0_ICON:
				player_0_move = self.userMove
				player_1_move = self.botMove
			else:
				player_0_move = self.botMove
				player_1_move = self.userMove
		# multiplayer
		else:
			print("{self.PLAYER_0_ICON}s plays first, decide who will be the first player.")
			player_0_move = self.userMove
			player_1_move = self.userMove

		return player_0_move, player_1_move

	def terminalGame(self):
		"""Starts a TikTacToe game in the terminal
		"""

		player_0_move, player_1_move = self.gameSettingsPrompt()
		
		# Start of game
		self.displayBoard()
		while True:
			print("First player's turn.")
			row, col = player_0_move(self.PLAYER_0_ICON)
			self.updateBoard(row, col, self.PLAYER_0_ICON)
			self.displayBoard()
			if self.game_state != self.NO_WINNER: break

			print("Second player's turn.")
			row, col = player_1_move(self.PLAYER_1_ICON)
			self.updateBoard(row, col, self.PLAYER_1_ICON)
			self.displayBoard()
			if self.game_state != self.NO_WINNER: break

		self.displayResult()
		self.resetGame()

	def displayBoard(self, blank_pos_color="\033[1;32m", exit_color_code="\033[0m"):
		"""Prints the board for the user to see.

		Takes no arguments and gives no return; rather, calls the self.board object directly and prints directly to console.
		"""

		result = "\n"
		for i in range(0, 9):
			row = floor(i / 3)
			col = i % 3
			if i in (0, 3, 6):
				if self.board[row][col] != self.BLANK_POS_ICON:
					result += f"\t {self.board[row][col]} ║"
				else:
					result += f"\t{blank_pos_color} {i + 1} {exit_color_code}║"
			elif i in (1, 4, 7):
				if self.board[row][col] != self.BLANK_POS_ICON:
					result += f" {self.board[row][col]} ║"
				else:
					result += f"{blank_pos_color} {i + 1} {exit_color_code}║"

			elif i in (2, 5, 8):
				if self.board[row][col] != self.BLANK_POS_ICON:
					result += f" {self.board[row][col]}\n"
				else:
					result += f"{blank_pos_color} {i + 1} {exit_color_code}\n"
				if i in (2, 5):
					result += "\t═══╬═══╬═══\n"

		print(result)

	def displayResult(self):
		"""Checks the give game_state and displays how the game ended.
		It takes in nothing and returns nothing
		"""

		if self.game_state == self.PLAYER_0_WINNER:
			print(f"{self.PLAYER_0_ICON} won the game!")
		elif self.game_state == self.PLAYER_1_WINNER:
			print(f"{self.PLAYER_1_ICON} won the game!")

		else:
			print("The game ended in a draw")

	def userMove(self, player_icon):
		"""Processes everything that is needed for a user to make a move, including checking if input was valid (through promptUser(), spot is free to move in, etc.)
	
		:param player_icon: The player_icon is not used in userMove but is necessary to avoid bugs with botMove.
					See how player_icon argument is used in botMove(self, player_icon),
					and how both of these functions are used in startTerminalGame(self) for details.
		"""

		valid_move = False
		row, col = 0, 0

		while not valid_move:
			row, col = self.promptUser()
			valid_move = self.checkValidMove(row, col)
			if not valid_move:
				print("That space is already taken")
		
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

if __name__ == "__main__":
	TicTacToe().terminalGame()
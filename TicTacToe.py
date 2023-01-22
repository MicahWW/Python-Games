import random
from datetime import datetime


##########################################################################################

# noinspection PyBroadException
class TicTacToe:
	"""Contains the objects and functions for running the TicTacToe game, to be called from main.py.

	Included functions:
		- __init__(self)
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

		# Why is random seed here?  For the bot to choose random moves?
		random.seed(datetime.now().strftime('%Y%m%d%H%M%S'))

		# Player Icons
		self.BLANK_POS_ICON = ' '
		self.PLAYER_0_ICON = 'X'
		self.PLAYER_1_ICON = 'O'
		# Game States
		self.NO_WINNER = 0
		self.X_WINNER = 1
		self.O_WINNER = 2
		self.DRAW_GAME = 3

		# Initialize empty board
		self.board = self.emptyBoard()

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
		"""Updates the board by assigning a player_icon to a given space.
		Does not return anything; assigns directly to the self.board object.

		:param row: the row of the space to be updated.
		:param col: the column of the space to be updated.
		:param player_icon: the icon to be put in the space (traditionally X or O).
		"""
		self.board[row][col] = player_icon

	def checkBoard(self):
		"""Checks the board for endgame scenarios, either a draw or a win by either player.

		:return: the state of the game, as one of the following:
			1. NO_WINNER (continue the game)
			2. X_WINNER (Player 0 wins)
			3. O_WINNER (Player 1 wins)
			4. DRAW_GAME
		"""
		# check for win in rows
		for row in range(0, 3):
			if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_0_ICON:
				return self.X_WINNER
			elif self.board[row][0] == self.board[row][1] == self.board[row][2] == self.PLAYER_1_ICON:
				return self.O_WINNER

		# check for win in columns
		for col in range(0, 3):
			if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_0_ICON:
				return self.X_WINNER
			elif self.board[0][col] == self.board[1][col] == self.board[2][col] == self.PLAYER_1_ICON:
				return self.O_WINNER

		# check for win in diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_0_ICON:
			return self.X_WINNER
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_0_ICON:
			return self.X_WINNER
		if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.PLAYER_1_ICON:
			return self.O_WINNER
		if self.board[2][0] == self.board[1][1] == self.board[0][2] == self.PLAYER_1_ICON:
			return self.O_WINNER

		# check if the board is full
		for row in self.board:
			for col in row:
				if col == self.BLANK_POS_ICON:
					return self.NO_WINNER

		return self.DRAW_GAME

	# behind the scenes functions
	##########################################################################################
	# terminal functions

	def startTerminalGame(self):
		"""Prints messages to allow the user to select number of players and player icon,
		then begins and runs the game by calling the necessary functions.

		This function is over 50 lines long, do we want to split it up some?
		I'm thinking single/multi-player selection can be it's own function, and maybe choosing player icons as well.
		Taking those two chunks and leaving only the last "start of game" block would put this around 20 lines.
		"""
		# choose the number of players
		num_players = 0
		while num_players != 1 and num_players != 2:
			try:
				num_players = int(input('Enter the number of players (1 or 2): '))
			except:
				pass
		
		# single player
		if num_players == 1:
			# choose the player icon
			player_choice = 0
			while player_choice != 'x' and player_choice != 'o':
				player_choice = input(f'{self.PLAYER_0_ICON}s plays first, do you want to be {self.PLAYER_0_ICON} or {self.PLAYER_1_ICON}? ')
				player_choice = player_choice.lower()

			# set the players based off the user's choice
			if player_choice == 'x':
				player_0_move = self.userMove
				player_1_move = self.botMove
			else:
				player_0_move = self.botMove
				player_1_move = self.userMove
		# multiplayer
		else:
			print(f'{self.PLAYER_0_ICON}s plays first, decide who will be the first player.')
			player_0_move = self.userMove
			player_1_move = self.userMove

		# Start of game
		self.displayBoard()
		while True:
			print('First player\'s turn.')
			row, col = player_0_move(self.PLAYER_0_ICON)
			self.updateBoard(row, col, self.PLAYER_0_ICON)
			self.displayBoard()
			game_state = self.checkBoard()
			if game_state != self.NO_WINNER:
				self.displayResult(game_state)
				break

			print('Second player\'s turn.')
			row, col = player_1_move(self.PLAYER_1_ICON)
			self.updateBoard(row, col, self.PLAYER_1_ICON)
			self.displayBoard()
			game_state = self.checkBoard()
			if game_state != self.NO_WINNER:
				self.displayResult(game_state)
				break

	def displayBoard(self):
		"""Prints the board for the user to see.

		Takes no arguments and gives no return; rather, calls the self.board object directly and prints directly to console.
		"""
		result = '     A | B | C \n\n'
		for idx_row, row in enumerate(self.board):
			result += str(idx_row) + '   '
			for idx_col, val in enumerate(row):
				result += ' '
				result += val
				
				if idx_col < 2:
					result += ' ║'
			if idx_row < 2:
				result += '\n    ═══╬═══╬═══\n'
		print(result)

	"""Checks the give game_state and displays how the game ended.
	
	:param game_state: the state that the game is in can be one of the below:
			1. NO_WINNER (continue the game)
			2. X_WINNER (Player 0 wins)
			3. O_WINNER (Player 1 wins)
			4. DRAW_GAME
			Option 1 (NO_WINNER) was included but nothing happens if that game state is passed
	"""
	def displayResult(self, game_state):
		if game_state == self.O_WINNER:
			print('O won the game!')
		elif game_state == self.X_WINNER:
			print('X won the game!')
		else:
			print('The game ended in a draw')

	"""Processes everything that is needed for a user to make a move, including checking if input was valid (through promptUser(), spot is free to move in, etc
	
	:param player_icon: The player_icon is not used in userMove but is necessary to avoid bugs with botMove.
					See how player_icon argument is used in botMove(self, player_icon),
					and how both of these functions are used in startTerminalGame(self) for details.
	"""
	def userMove(self, player_icon):
		# The player_icon is not used in userMove but is necessary to avoid bugs with botMove.
		# See how player_icon argument is used in botMove(self, player_icon),
		# and how both of these functions are used in startTerminalGame(self) for details.
		valid_move = False
		row, col = 0, 0

		while not valid_move:
			row, col = self.promptUser()
			valid_move = self.checkValidMove(row, col)
			if not valid_move:
				print('That space is already taken')
		
		return row, col

	@staticmethod
	def promptUser():
		"""Requests user input for desired move on user's turn, validates, and then returns selected space.

		:return: (row, col) as the row and column of the space selected by the user for their move.
		"""
		while True:
			choice = input('Where do you want to play? ')
			if len(choice) == 2:
				choice = choice.lower()
				if choice[0] in ['a', 'b', 'c']:
					col = choice[0]
				elif choice[1] in ['a', 'b', 'c']:
					col = choice[1]
				else:
					col = ''

				if choice[0] in ['0', '1', '2']:
					row = choice[0]
				elif choice[1] in ['0', '1', '2']:
					row = choice[1]
				else:
					row = ''
			
				if row != '' and col != '':
					if col == 'a':
						col = 0
					elif col == 'b':
						col = 1
					# Does the use of "else" here open us up to a bug where the last column is selected in a weird scenario?
					# Going through the logic it seems solid to me but if it were obvious it wouldn't really be a bug, would it?
					else:
						col = 2

					row = int(row)
					return row, col

			print('Invalid answer')

	def botMove(self, player_icon):
		"""The brains of the most badass, unbeatable bot this side of the singularity.
		Okay probably not, but it should at least block easy wins.

		:param player_icon: either self.PLAYER_0_ICON or self.PLAYER_1_ICON, used by the bot to distinguish user from bot.
		:return: (row, col) as integers representing the row and column of bot's desired move."""

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

if __name__ == "__main__":
	TicTacToe().startTerminalGame()

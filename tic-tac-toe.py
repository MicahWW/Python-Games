from enum import Enum
import sys
import random
from datetime import datetime

class PlayerValues(Enum):
	BLANK_POS		= 0
	X_PLAYER		= 1
	O_PLAYER		= 2

class GameStates(Enum):
	NO_WINNER		= 0
	X_WINNER		= 1
	O_WINNER		= 2
	DRAW_GAME		= 3

##########################################################################################
# functions


def emptyBoard():
	return [
		[PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value],
		[PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value],
		[PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value, PlayerValues.BLANK_POS.value]

		]


def displayBoard(board):
	result = '     A | B | C \n\n'
	for idx_row, row in enumerate(board):
		result += str(idx_row) + '   '
		for idx_col, val in enumerate(row):
			result += ' '
			if val == PlayerValues.BLANK_POS.value:
				result += ' '
			elif val == PlayerValues.X_PLAYER.value:
				result += 'X'
			elif val == PlayerValues.O_PLAYER.value:

				result += 'O'
			else:
				# TODO: how to error handel
				sys.exit()
			if idx_col < 2:
				result += ' ║'
		if idx_row < 2:
			result += '\n    ═══╬═══╬═══\n'
	print(result)


def promptUser():
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
				else:
					col = 2

				row = int(row)
				return row, col

		print('Invalid answer')


def checkValidMove(row, col, board):
	return board[row][col] == PlayerValues.BLANK_POS.value


def userMove(board):
	valid_move = False
	row, col = '', ''

	while not valid_move:
		row, col = promptUser()
		valid_move = checkValidMove(row, col, board)
		if not valid_move:
			print('That space is already taken')

	return row, col



def updateBoard(row, col, board, player_icon):
	if isinstance(player_icon, PlayerValues):
		board[row][col] = player_icon.value

	else:
		# TODO: how to error handel
		sys.exit()


def botMove(board):
	valid_move = False
	row, col = 0, 0

	while not valid_move:
		row = random.choice([0, 1, 2])
		col = random.choice([0, 1, 2])
		valid_move = checkValidMove(row, col, board)

	return row, col


def checkBoard(board):
	# check for win in rows
	for row in range(0, 3):
		if board[row][0] == board[row][1] == board[row][2] == PlayerValues.X_PLAYER.value:
			return GameStates.X_WINNER
		elif board[row][0] == board[row][1] == board[row][2] == PlayerValues.O_PLAYER.value:
			return GameStates.O_WINNER

	# check for win in columns
	for col in range(0, 3):
		if board[0][col] == board[1][col] == board[2][col] == PlayerValues.X_PLAYER.value:
			return GameStates.X_WINNER
		elif board[0][col] == board[1][col] == board[2][col] == PlayerValues.O_PLAYER.value:
			return GameStates.O_WINNER

	# check for win in diagonals
	if board[0][0] == board[1][1] == board[2][2] == PlayerValues.X_PLAYER.value:
			return GameStates.X_WINNER
	if board[2][0] == board[1][1] == board[0][2] == PlayerValues.X_PLAYER.value:
			return GameStates.X_WINNER
	if board[0][0] == board[1][1] == board[2][2] == PlayerValues.O_PLAYER.value:
			return GameStates.O_WINNER
	if board[2][0] == board[1][1] == board[0][2] == PlayerValues.O_PLAYER.value:
			return GameStates.O_WINNER

	# check if the board is full
	for row in board:
		for col in row:
			if col == PlayerValues.BLANK_POS.value:
				return GameStates.NO_WINNER

	return GameStates.DRAW_GAME

def displayResult(game_state):
	if game_state == GameStates.O_WINNER:
		print('O won the game!')
	elif game_state == GameStates.X_WINNER:
		print('X won the game!')
	else:
		print('The game ended in a draw')

# functions
##########################################################################################
# run the game
def playTikTacToe():
	random.seed(datetime.now().strftime('%Y%m%d%H%M%S'))
	# print('The Xs play first') # TODO: make the Xs play first
	# user = input('Do you want to be Xs or Os? ')
	# user = user.lower()
	print('When making a choice use 1, 2, or 3 for a row and A, B, or C for a column')
	print('When entering your choice it must only have one row selection and one column selection with nothing else.')
	print('EX: A1 or 3B')

	board = emptyBoard()
	displayBoard(board)


	while True:
		row, col = userMove(board)
		updateBoard(row, col, board, PlayerValues.X_PLAYER)
		displayBoard(board)
		game_state = checkBoard(board)
		if game_state != GameStates.NO_WINNER:
			displayResult(game_state)
			break

		print ('Processing bot\'s move')
		row, col = botMove(board)
		updateBoard(row, col, board, PlayerValues.O_PLAYER)
		displayBoard(board)
		game_state = checkBoard(board)
		if game_state != GameStates.NO_WINNER:
			displayResult(game_state)
			break



if __name__ == "__main__":
	playTikTacToe()
from enum import Enum
import sys
import random
from datetime import datetime


class PlayerValues(Enum):
	BLANK_POS		= 0
	X_PLAYER		= 1
	O_PLAYER		= 2

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
	row, col = '', ''

	while not valid_move:
		row = random.choice([0, 1, 2])
		col = random.choice([0, 1, 2])
		valid_move = checkValidMove(row, col, board)

	return row, col


# functions
##########################################################################################
# run the game
def playTikTacToe():
	# print ('The Xs play first') # TODO: make the Xs play first
	# user = input('Do you want to be Xs or Os? ')
	# user = user.lower()
	print('When making a choice use 1, 2, or 3 for a row and A, B, or C for a column')
	print('When entering your choice it must only have one row selection and one column selection with nothing else.')
	print('EX: A1 or 3B')

	board = emptyBoard()
	user_moves = 0

	while True:
		random.seed(datetime.now().strftime('%Y%m%d%H%M%S'))
		displayBoard(board)
		row, col = userMove(board)
		updateBoard(row, col, board, PlayerValues.X_PLAYER)

		# Keep track of player moves.  If user moves first, they will move 5 times, after which the game ends.
		# TODO: if bot moves first, this will need to accommodate 5 bot moves / 4 player moves.  Figure out how this will work.
		# Maybe TODO: do we want this feature to be it's own function?  Does it work better inside this function?
		user_moves += 1
		if user_moves == 5:
			displayBoard(board)
			break
		row, col = botMove(board)
		updateBoard(row, col, board, PlayerValues.O_PLAYER)


if __name__ == "__main__":
	playTikTacToe()
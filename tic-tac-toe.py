from enum import Enum
import sys
import random
from datetime import datetime

class playerIcons(Enum):
	BLANK_ICON	= 0
	X_ICON		= 1
	O_ICON		= 2


##########################################################################################
# functions

def emptyBoard():
	return [
		[playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value],
		[playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value],
		[playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value, playerIcons.BLANK_ICON.value]
		]

def displayBoard(board):
	result = '     A | B | C \n\n'
	for idx_row, row in enumerate(board):
		result += str(idx_row) + '   '
		for idx_col, val in enumerate(row):
			result += ' '
			if val == playerIcons.BLANK_ICON.value:
				result += ' '
			elif val == playerIcons.X_ICON.value:
				result += 'X'
			elif val == playerIcons.O_ICON.value:
				result += 'O'
			else:
				# TODO: how to error handel
				sys.exit()
			if idx_col < 2:
				result += ' ║'
		if idx_row < 2:
			result += '\n    ═══╬═══╬═══\n'
	print (result)

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

		print ('Invalid answer')

def checkValidMove(row, col, board):
	return board[row][col] == playerIcons.BLANK_ICON.value

def userMove(board):
	validMove = False

	while not validMove:
		row, col = promptUser()
		validMove = checkValidMove(row, col, board)
		if not validMove:
			print ('That space is already taken')

	return row, col

def updateBoard(row, col, board, playerIcon):
	if isinstance(playerIcon, playerIcons):
		board[row][col] = playerIcon.value
	else:
		# TODO: how to error handel
		sys.exit()

def botMove(board):
	validMove = False

	while not validMove:
		row = random.choice([0, 1, 2])
		col = random.choice([0, 1, 2])
		validMove = checkValidMove(row, col, board)

	return row, col


# functions
##########################################################################################
# run the game
def playTikTacToe():
	#print ('The Xs play first') # TODO: make the Xs play first
	#user = input('Do you want to be Xs or Os? ')
	#user = user.lower()
	print ('When making a choice use 1, 2, or 3 for a row and A, B, or C for a column')
	print ('When entering your choice it must only have one row selection and one column selection with nothing else.')
	print ('EX: A1 or 3B')

	board = emptyBoard()


	while True:
		random.seed(datetime.now().strftime('%Y%m%d%H%M%S'))
		displayBoard(board)
		row, col = userMove(board)
		updateBoard(row, col, board, playerIcons.X_ICON)
		row, col = botMove(board)
		updateBoard(row, col, board, playerIcons.O_ICON)



if __name__ == "__main__":
	playTikTacToe()
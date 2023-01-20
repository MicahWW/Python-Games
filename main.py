from sys import exit
from TicTacToe import TicTacToe

games = [TicTacToe()]

cont = True
while cont:
	print(f'There are {len(games)} games...')
	for idx, game in enumerate(games):
		print(f'{idx}: {game.gameName()}')

	selection = -1
	while not (0 <= selection < len(games)):
		print('To exit type \'exit\'')
		selection = input('Which do you want to play? ')

		try:
			selection = int(selection)
		except:
			if selection.lower() == 'exit':
				exit(0)
	games[selection].terminalGame()
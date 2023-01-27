from sys import exit
from TicTacToe import TicTacToe

games = [TicTacToe()]

while True:
	print(f'There are {len(games)} games...')
	for idx, game in enumerate(games, start=1):
		print(f'{idx}: {game.gameName()}')

	selection = -1
	while not (0 <= selection < len(games)):
		print('\nWhich do you want to play?')
		selection = input('To select a game enter it\'s number, or to exit enter \'exit\': ')

		if selection.isnumeric():
			selection = int(selection) - 1
		elif selection == 'exit':
			exit(0)
		else:
			print('Invalid input')
			continue

		if selection < len(games):
			cont = True
			while cont:
				games[selection].terminalGame()
				cont = input('Would you like to play this game again? (y/n): ')
				cont = True if cont.lower() == 'y' else False
		else:
			print('There are not that many games!')
			continue
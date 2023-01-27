from sys import exit
from TicTacToe import TicTacToe

games = [TicTacToe()]

while True:
	print(f'There are {len(games)} games...')
	for idx, game in enumerate(games, start=1):
		print(f'{idx}: {game.gameName()}')

	selection = -1
	while not (0 < selection < len(games)):
		print('To exit type \'exit\'\n')
		selection = input('Which do you want to play?\nEnter game number: ')

		try:
			selection = int(selection) - 1
			games[selection].terminalGame()
			cont = input("Would you like to play again? (y/n): ")
			while cont.lower() == "y":
				games[selection].terminalGame()
				cont = input("Would you like to play again? (y/n): ")
			reselect = input("Would you like to play a different game? (y/n): ")
			if reselect.lower() == "y":
				pass
			else:
				exit(0)
		except ValueError:
			if selection.lower() == 'exit':
				exit(0)
			else:
				print(f'Please enter a number between 1 and {len(games)}, or enter "exit" to quit.\n')
				selection = -1
		except IndexError:
			print('There are not that many games!')
			print(f'Please enter a number between 1 and {len(games)}, or enter "exit" to quit.\n')

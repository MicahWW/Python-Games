from sys import exit
import TicTacToe

games = [TicTacToe.TicTacTerminal()]

while True:
	print(f"There are {len(games)} games...")
	for idx, game in enumerate(games, start=1):
		print(f"{idx}: {game.gameName()}")

	while True:
		print("\nWhich do you want to play?")
		selection = input("To select a game enter it's number, or to exit enter 'exit': ")

		if selection.isnumeric():
			selection = int(selection) - 1
			if selection < len(games):
				cont = True
				while cont:
					games[selection].terminalGame()
					cont = input("Would you like to play this game again? (y/n): ")
					cont = True if cont.lower() == "y" else False
				break
			else:
				print("There are not that many games!")
				continue
		elif selection == "exit":
			exit(0)
		else:
			print("Invalid input")
			continue

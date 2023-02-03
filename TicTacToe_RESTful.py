import TicTacToe
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
game = TicTacToe.TicTacToe()

@app.route("/game_name", methods=["GET"])
def game_name_route():
	return game.gameName()




if __name__ == "__main__":
	app.run()
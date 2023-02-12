import TicTacToe
from flask import Flask, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
game = TicTacToe.TicTacToe()

@app.route("/gameName", methods=["GET"])
def gameName_route():
	return json.dumps(game.gameName())

@app.route("/board", methods=["GET"])
def currentBoard_route():
	return json.dumps(game.board)

@app.route("/checkValidMove", methods=["POST"])
def checkValidMove_route():
	query = request.get_json()
	row = query.get("row", "error")
	col = query.get("col", "error")

	if row == "error" or col == "error":
		print("Move was invalid, recieved:")
		print(f"row:\t{row}\ncol:\t{col}")
		print(f"query:\t{query}")
		return {"valid": False}
	return {"valid": game.checkValidMove(row, col)}

@app.route("/updateBoard", methods=["POST"])
def updateBoard_route():
	query = request.get_json()
	row = query.get("row", "error")
	col = query.get("col", "error")
	player = query.get("player", "error")

	if row == "error" or col == "error" or player == "error":
		print("Move was invalid, recieved:")
		print(f"row:\t{row}\ncol:\t{col}\nplayer:\t{player}")
		print(f"query:\t{query}")
		return {"updated": False}
	game.updateBoard(row, col, player)
	game.checkBoard()
	return {"updated": True, "game_state": game.game_state}

@app.route("/botMove", methods=["POST"])
def botMove_route():
	query = request.get_json()
	player = query.get("player", "error")

	if player == "error":
		print(f"player:\t{player}")
		print(f"query:\t{query}")
		return {"valid: False"}
	row, col = game.botMove(player)
	return {"valid": True, "row": row, "col": col}

@app.route("/resetGame", methods=["POST"])
def resetGame_route():
	global game
	game = TicTacToe.TicTacToe()
	return json.dumps(game.board)

@app.route("/gameState", methods=["GET"])
def gameState_route():
	return {"game_state": game.game_state}


if __name__ == "__main__":
	app.run()
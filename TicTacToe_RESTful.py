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
	row = query.get('row', -1)
	col = query.get('col', -1)

	if row == -1 or col == -1:
		return {'valid': False}
	return {'valid': game.checkValidMove(row, col)}

@app.route("/updateBoard", methods=["POST"])
def updateBoard_route():
	query = request.get_json()
	row = query.get('row', -1)
	col = query.get('col', -1)

	if row == -1 or col == -1:
		return {'updated': False}
	game.updateBoard(row, col, -1)
	return {'updated': True}

if __name__ == "__main__":
	app.run()
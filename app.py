from flask import Flask, render_template, jsonify
import numpy as np
import math
from game import minimax, HUMAN_PIECE, AI_PIECE, dropPiece

BOARD_ROW = 6
BOARD_COL = 7

board = np.zeros((BOARD_ROW, BOARD_COL))
app = Flask(__name__)
@app.route('/')
def home():
    global board
    board = np.zeros((BOARD_ROW, BOARD_COL))
    return render_template("index.html")

@app.route('/ai-move')
def aiMove():
    result = minimax(board, 7, -math.inf, math.inf, True)
    move = result[0]
    dropPiece(board, move, AI_PIECE)
    return jsonify({"move": move}) 

@app.route('/human-move/<col>')
def humanMove(col):
    dropPiece(board, int(col), HUMAN_PIECE)
    return jsonify({"move": col})
if __name__ == '__main__':
    app.run()
